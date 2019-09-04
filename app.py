import os
import os.path as op
from datetime import datetime
from flask import Flask
from flask_cors import CORS
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import Response
import africastalking
import json

import flask_admin as admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
# TODO(aashni): check if CORS setup is correct
CORS(app)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
username = "sandbox"
api_key = os.environ.get('AT_API_KEY')
test_number = "+254456923994"
africastalking.initialize(username, api_key)
sms = africastalking.SMS


def test_text():
  africastalking.initialize(username, api_key)

  # Initialize a service e.g. SMS
  sms = africastalking.SMS

  # Use the service synchronously
  try:
    response = sms.send("~*~*~Testing text send from Africa's Talking API~*~*~", [test_number])
    print(response)
  except Exception as e:
    print('Encountered an error while sending: %s' % str(e))


def get_members(from_user):
  user_phone = int(from_user)
  print('User phone: ' + str(user_phone))
  officer_role = Role.query.filter(Role.name == "officer").first()
  valid_user = User.query.filter(User.role_id == officer_role.id, User.phone == user_phone).first()
  valid = False
  if valid_user is not None:
    valid = True
  if not valid:
    return "Error: you are not an officer"
  coop = CoOp.query.filter(CoOp.id == valid_user.co_op_id).first()
  users = User.query.filter(User.co_op_id == coop.id)
  members = 'Members in your coop:\n'
  for user in users:
    members += user.first_name + ' ' + user.last_name + ': (id = ' + str(user.id) + ')\n'
  return members


def add_transaction(from_user, msg):
  leader_phone = int(from_user)
  print(leader_phone)
  leader = User.query.filter(User.phone == leader_phone).first()
  # TODO: check to make sure user exists, is leader
  member_phone = msg[1]
  member = User.query.filter(User.phone == member_phone).first()
  if member == None:
    return send_error(leader_phone)
  amount = int(msg[2])
  loan_balance = member.loan.balance
  new_user_transaction = Transaction(
    loan=[member.loan],
    amount=amount,
    previous_balance=loan_balance,
    new_balance=loan_balance - amount,
    state='initiated',
    user_id=member.id
  )
  member.transactions.append(new_user_transaction)
  db.session.add(member)
  db.session.add(new_user_transaction)
  db.session.commit()
  africastalking.initialize(username, api_key)
  sms = africastalking.SMS
  try:
    leader_text = sms.send("Transaction added. Requesting confirmation from " + str(member_phone),
                           ['+' + str(leader_phone)])
    member_text = sms.send("Your Co-Op Leader has added a " + str(amount) + " repayment transaction for your loan. \
    Please respond with 'Y' to confirm this transaction is accurate or 'N' to reject it. Your new balance will be: " + str(
      loan_balance - amount), ['+' + str(member_phone)])
    print(leader_text)
    print(member_text)
    return 'success: added loan transaction'
  except Exception as e:
    print('Encountered an error while sending: %s' % str(e))
    return 'Encountered an error while sending: %s' % str(e)


def send_error(sender_phone):
  error_text = sms.send(
    "The user you are trying to update does not exist in our database. Please text <ADD {user number}> if you would like to add them",
    ['+' + str(sender_phone)])
  print(error_text)
  return 'error: user does not exist'


def confirm_transaction(from_user):
  member = User.query.filter(User.phone == int(from_user)).first()
  # TODO: return error message if user does not exist
  user_transaction = member.transactions.all()[-1]
  # TODO: return notice message if transaction has already been confirmed
  if user_transaction.state == 'initiated':
    user_transaction.state = 'confirmed'
    member.loan.balance = user_transaction.new_balance

    db.session.add(member)
    db.session.add(user_transaction)
    db.session.commit()
    try:
      member_text = sms.send("Transaction complete. New loan balance is " + str(member.loan.balance), [from_user])
      print(member_text)
    except Exception as e:
      print('Encountered an error while sending: %s' % str(e))


# Models
roles_users = db.Table(
  'roles_users',
  db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
  db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

co_ops_users = db.Table(
  'co_ops_users',
  db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
  db.Column('co_op_id', db.Integer(), db.ForeignKey('co_op.id'))
)

loans_users = db.Table(
  'loans_users',
  db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
  db.Column('loan_id', db.Integer, db.ForeignKey('loan.id'))
)

transactions_loans = db.Table(
  'transactions_loans',
  db.Column('transaction_id', db.Integer, db.ForeignKey('transaction.id')),
  db.Column('loan_id', db.Integer, db.ForeignKey('loan.id'))
)

transactions_users = db.Table(
  'transactions_users',
  db.Column('transaction_id', db.Integer, db.ForeignKey('transaction.id')),
  db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)


class CoOp(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(80), unique=True)
  is_active = db.Column(db.Boolean())
  start_date = db.Column(db.DateTime())
  end_date = db.Column(db.DateTime())
  location = db.Column(db.String(255))
  interest = db.Column(db.Integer())
  initial_balance = db.Column(db.Integer())
  expected_repayment = db.Column(db.Integer())
  current_balance = db.Column(db.Integer())
  users = db.relationship('User', uselist=False, backref='co_op')

  def __str__(self):
    return self.name


class Role(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(80), unique=True)
  description = db.Column(db.String(255))
  users = db.relationship('User', uselist=False, backref='role')

  def __str__(self):
    return self.name


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(255))
  last_name = db.Column(db.String(255))
  email = db.Column(db.String(255), unique=True)
  phone = db.Column(db.String(255), unique=True)
  password = db.Column(db.String(255))
  active = db.Column(db.Boolean())
  confirmed_at = db.Column(db.DateTime())
  co_op_id = db.Column(db.Integer, db.ForeignKey('co_op.id'))
  role_id = db.Column('Role', db.ForeignKey('role.id'))
  loan = db.relationship('Loan', uselist=False, backref='user')
  transactions = db.relationship('Transaction', secondary=transactions_users,
                                 backref='users', lazy='dynamic')

  def __str__(self):
    return self.email


class Loan(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  balance = db.Column(db.Integer)
  interest = db.Column(db.Integer)
  loan_start = db.Column(db.DateTime)
  loan_end = db.Column(db.DateTime)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Transaction(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  amount = db.Column(db.Integer)
  previous_balance = db.Column(db.Integer)
  new_balance = db.Column(db.Integer)
  state = db.Column(db.String(255))
  timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  loan = db.relationship('Loan', secondary=transactions_loans,
                         backref=db.backref('transactions', lazy='dynamic'))


# Customized admin interface
class CustomView(ModelView):
  list_template = 'list.html'
  create_template = 'create.html'
  edit_template = 'edit.html'


class UserAdmin(CustomView):
  column_searchable_list = ()
  column_filters = ('first_name', 'email')
  column_exclude_list = ['password', ]


# Flask views
@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'GET':
    return '<a href="/admin/">Click me to get to Admin!</a>'

  # text receive
  if request.method == 'POST':
    try:
      from_user = request.form.getlist('from')[0]
      print(from_user)
    except:
      from_user = None
    if from_user == None:
      return 'failure: request error'
    msg = request.form.getlist('text')[0].split()
    cmd = msg[0]
    print(msg)
    print(cmd)
    if cmd.lower() == 'loan':
      if len(msg) != 3:
        return 'error'
      return add_transaction(from_user, msg)
    elif cmd.lower() == 'y':
      confirm_transaction(from_user)
    elif cmd.lower() == 'n':
      return 'transaction denied'
      # TODO: remove transaction
    elif cmd == 'MEMBERS':
      list_of_members = get_members(from_user)
      print(list_of_members)
      response = sms.send(list_of_members, [from_user])
      print(response)
    else:
      return 'error'
      # TODO: handle error
    # ImmutableMultiDict([
    #   ('linkId', '04c0d31e-e16a-42b9-aa3b-2157c79e4c82'),
    #   ('text', '254987654321 LOAN 500'),
    #   ('to', '7635'),
    #   ('id', '86b65912-d4ac-44f3-b912-c7a046134836'),
    #   ('date', '2019-02-03 09:52:15'),
    #   ('from', '+254123456789')
    #   ])
    print(request.form)
    return 'success'


@app.route('/transactions', methods=['GET'])
def transactions():
  data = []
  transactions = Transaction.query.order_by(Transaction.timestamp.desc()).all()
  for transaction in transactions:
    user = User.query.filter(User.id == transaction.user_id).first()
    data.append(
      {
        "amount": transaction.amount,
        "previous_balance": transaction.previous_balance,
        "new_balance": transaction.new_balance,
        "state": transaction.state,
        "user_name": user.first_name + ' ' + user.last_name,
        "timestamp": transaction.timestamp
      }
    )
  results = {"data": data}

  return Response(json.dumps(results, default=str), mimetype='application/json')


@app.route('/members', methods=['GET'])
def members():
  data = []
  users = User.query.all()
  for user in users:
    data.append(
      {
        "name": user.first_name + ' ' + user.last_name,
        "coop": CoOp.query.filter(CoOp.id == user.co_op_id).first().name,
        "phone": user.phone,
        "role": Role.query.filter(Role.id == user.role_id).first().name,
        "loan_balance": user.loan.balance if user.loan else 'N/A'
      }
    )
  results = {"data": data}

  return Response(json.dumps(results, default=str), mimetype='application/json')


@app.route('/coops', methods=['GET'])
def coops():
  data = []
  coops = CoOp.query.all()
  for coop in coops:
    data.append(
      {
        "name": coop.name,
        "start_date": coop.start_date,
        "end_date": coop.end_date,
        "location": coop.location,
        "interest": coop.interest,
        "initial_balance": coop.initial_balance,
        "current_balance": coop.current_balance,
        "expected_repayment": coop.expected_repayment
      }
    )
  results = {"data": data}

  return Response(json.dumps(results), mimetype='application/json')


# Admin interface
admin = admin.Admin(app, name='Pangea Network', template_mode='bootstrap3')

# Add views
admin.add_view(CustomView(CoOp, db.session, name="Co Ops"))
admin.add_view(CustomView(Role, db.session, name="Roles"))
admin.add_view(CustomView(Transaction, db.session, name="Transactions"))
admin.add_view(CustomView(Loan, db.session, name="Loans"))
admin.add_view(UserAdmin(User, db.session, name="Users"))


def build_sample_db():
  """
Populate a small db with some example entries.
"""

  import string
  import random

  db.drop_all()
  db.create_all()

  with app.app_context():
    user_role = Role(name='member')
    super_user_role = Role(name='officer')
    db.session.add(user_role)
    db.session.add(super_user_role)
    db.session.commit()

    co_op_1 = CoOp(
      name='ABC',
      is_active=True,
      location='Seattle',
      interest=5,
      initial_balance=2000,
      expected_repayment=2200,
      current_balance=1500
    )

    co_op_2 = CoOp(
      name='DEF',
      is_active=True,
      location='New York',
      interest=5,
      initial_balance=4000,
      expected_repayment=4400,
      current_balance=35000
    )

    db.session.add(co_op_1)
    db.session.add(co_op_2)
    db.session.commit()

    admin_user = User(
      first_name='Admin',
      last_name='User',
      email='admin',
      password='admin',
      phone='254798745678',
      role_id=super_user_role.id,
      co_op_id=co_op_1.id
    )
    test_user = User(
      first_name='Test',
      last_name='User',
      email='test@user.com',
      password='12345',
      phone='254987654321',
      role_id=user_role.id,
      co_op_id=co_op_1.id
    )
    db.session.add(admin_user)
    db.session.add(test_user)
    db.session.commit()

    test_user_loan = Loan(
      user=test_user,
      balance=2000,
      interest=2,
    )
    db.session.add(test_user_loan)
    db.session.commit()

  return


if __name__ == '__main__':

  # Build a sample db on the fly, if one does not exist yet.
  app_dir = os.path.realpath(os.path.dirname(__file__))
  database_path = os.path.join(app_dir, app.config['DATABASE_FILE'])
  if not os.path.exists(database_path):
    build_sample_db()
  test_text()

  # Start app
  app.run(debug=True)
