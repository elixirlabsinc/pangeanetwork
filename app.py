import os
import os.path as op
from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
import africastalking

import flask_admin as admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

username = "sandbox"   
api_key = os.environ.get('AT_API_KEY')   
test_number = "+254723963007"  

def test_text():
  africastalking.initialize(username, api_key)

  # Initialize a service e.g. SMS
  sms = africastalking.SMS

  # Use the service synchronously
  try:
    response = sms.send("Hello Message!", [test_number])
    print (response)
  except Exception as e:
    print ('Encountered an error while sending: %s' % str(e))

def add_transaction(data):
  user_phone = data.getlist('from')[0]
  user = User.query.filter(User.phone == user_phone).first()
  amount = int(data.getlist('text')[0].split()[1])
  loan_balance = user.loan.balance
  new_user_transaction = Transaction(
    loan=[user.loan],
    user=[user],
    amount=amount,
    previous_balance=loan_balance,
    new_balance=loan_balance - amount
  )
  db.session.add(new_user_transaction)
  db.session.commit()

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

  def __str__(self):
    return self.name


class Role(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(80), unique=True)
  description = db.Column(db.String(255))

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
  loan = db.relationship('Loan', uselist=False, backref='user')
  co_ops = db.relationship('CoOp', secondary=co_ops_users,
                          backref=db.backref('users', lazy='dynamic'))
  roles = db.relationship('Role', secondary=roles_users,
                          backref=db.backref('users', lazy='dynamic'))

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
  loan = db.relationship('Loan', secondary=transactions_loans,
                          backref=db.backref('transactions', lazy='dynamic'))
  user = db.relationship('User', secondary=transactions_users,
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
@app.route('/', methods = ['GET', 'POST'])
def index():
  if request.method == 'GET':
    return '<a href="/admin/">Click me to get to Admin!</a>'
  if request.method == 'POST':
    msg = request.form.getlist('text')
    cmd = msg[0].split()[0]
    if cmd.lower() == 'loan':
      add_transaction(request.form)
      return 'success: added loan transaction'
    # ImmutableMultiDict([
    #   ('linkId', '04c0d31e-e16a-42b9-aa3b-2157c79e4c82'), 
    #   ('text', 'LOAN 500'), 
    #   ('to', '7635'), 
    #   ('id', '86b65912-d4ac-44f3-b912-c7a046134836'), 
    #   ('date', '2019-02-03 09:52:15'), 
    #   ('from', '+254723963007')
    #   ])
    print(data)
    return 'success'


@app.route('/get_messages')
def get_messages():
  test_receive()
  return 'message sent!'
  

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
      phone='+254723963000',
      roles=[super_user_role]
    )
    test_user = User(
      first_name='Test',
      last_name='User',
      email='test@user.com',
      password='12345',
      phone=test_number,
      roles=[user_role]
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

    test_user_transaction = Transaction(
      loan=[test_user_loan],
      user=[test_user],
      amount=50,
      previous_balance=2000,
      new_balance=1950
    )
    db.session.add(test_user_transaction)
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
