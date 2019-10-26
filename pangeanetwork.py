from app import create_app, db
import os
import os.path as op
from datetime import datetime
from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from passlib.hash import pbkdf2_sha256 as sha256
from app.models import User, CoOp, Role, Loan, Transaction
import africastalking
import json

app = create_app()
jwt = JWTManager(app)

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
  africastalking.initialize(username, api_key)
  sms = africastalking.SMS
  from_phone = int(from_user)
  print(from_phone)
  member_id = msg[1]
  member = User.query.filter(User.id == member_id).first()
  if member == None:
    return send_missing_user_error(from_phone)
  amount = int(msg[2])
  if member.loan == None:
    officer_text = sms.send('ERROR: Given member does not have a current loan', [from_phone])
    print(officer_text)
    return 'Error: Member does not have a current loan'
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
  officer_role = Role.query.filter(Role.name == "officer").first()
  co_op_officer = User.query.filter(User.role_id == officer_role.id, User.co_op_id == member.co_op_id).first()
  
  try:
    response_text = sms.send("Transaction added. Requesting confirmation from Co-Op Leader", ['+' + str(from_phone)])
    leader_text = sms.send("A new repayment transaction has been added for member " + str(member.first_name) + " (ID: " + str(member.id) + ") in the amount of " + str(amount) + ". \
    Please respond with 'Y " + str(member.id) + "' to confirm this transaction is accurate or 'N " + str(member.id) + "' to reject it. Their new balance will be: " + 
    str(loan_balance - amount), ['+' + co_op_officer.phone])
    print(response_text)
    print(leader_text)
    return 'success: added loan transaction'
  except Exception as e:
    print('Encountered an error while sending: %s' % str(e))
    return 'Encountered an error while sending: %s' % str(e)


def send_missing_user_error(sender_phone):
  error_text = sms.send(
    "The user you are trying to update does not exist in our database. Please text <ADD {user number}> if you would like to add them", ['+' + str(sender_phone)])
  print(error_text)
  return 'error: user does not exist'


def confirm_transaction(from_user, msg):
  officer = User.query.filter(User.phone == int(from_user)).first()
  # TODO: return error message if user does not exist
  # TODO: return error message if user is not an officer
  member_id = msg[1]
  co_op = CoOp.query.filter(CoOp.id == officer.co_op_id).first()
  member = User.query.filter(User.co_op_id == co_op.id, User.id == member_id).first()
  if member == None:
    return send_missing_user_error(from_user)
  user_transaction = member.transactions.all()[-1]
  if user_transaction == None:
    error_text = sms.send('ERROR: There is no transaction available to confirm for user ' + str(member.first_name))
    print(error_text)
    return 'error: transaction does not exist'
  elif user_transaction.state == 'initiated':
    user_transaction.state = 'confirmed'
    member.loan.balance = user_transaction.new_balance
    co_op.current_balance -= user_transaction.amount
    db.session.add(member)
    db.session.add(co_op)
    db.session.add(user_transaction)
    db.session.commit()
    try:
      officer_text = sms.send("Transaction complete. New balance for member " + str(member.id) + ' - ' + str(member.first_name) + " is " + str(member.loan.balance) + '. \
        New balance for Co-Op ' + co_op.name + ' is ' + str(co_op.current_balance), [from_user])
      if member.phone:
        member_text = sms.send('Transaction confirmed. Your new balance is ' + str(member.loan.balance), [member.phone])
        print(member_text)
      print(officer_text)
    except Exception as e:
      print('Encountered an error while sending: %s' % str(e))

def create_new_user(user_data):
  new_user = User(
    first_name=user_data['first_name'],
    last_name=user_data['last_name'],
    email=user_data['email'],
    phone=user_data['phone'],
    active=True,
    co_op_id=user_data['co_op_id'],
    role_id=user_data['role_id']
  )
  db.session.add(new_user)
  db.session.commit()
  return new_user.id


# Routes
@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'GET':
    return 'success'
  
  if request.method == 'POST': # text receive
    data = request.form.to_dict()
    # expected data format: 
    # {'linkId': 'xxxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx', 
    # 'text': 'loan 2 34', 
    # 'to': '<short code>', 
    # 'id': 'xxxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx', 
    # 'date': '2019-10-02 15:12:34', 
    # 'from': '+11234567890}
    try:
      from_user = data['from']
      print(from_user)
    except:
      from_user = None
    if from_user == None:
      return 'failure: request error'
    msg = data['text'].split()
    cmd = msg[0].lower()
    print(msg)
    print(cmd)
    if cmd == 'loan':
      if len(msg) != 3:
        return 'error'
      return add_transaction(from_user, msg)
    elif cmd == 'y':
      confirm_transaction(from_user, msg)
    elif cmd == 'n':
      return 'transaction denied'
      # TODO: remove transaction
    elif cmd == 'members':
      list_of_members = get_members(from_user)
      print(list_of_members)
      response = sms.send(list_of_members, [from_user])
      print(response)
    # TODO: support 'new' command for new members and funds
    else:
      return 'error'
      # TODO: handle error
    return 'success'


@app.route('/transactions', methods=['GET'])
@jwt_required
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


@app.route('/members', methods=['GET', 'POST'])
@jwt_required
def members():
  if request.method == 'GET':
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

  elif request.method == 'POST':
    data = request.form.to_dict()
    id = create_new_user(data)
    result = { 'status': 200, 'user_id': id }
    # TODO: prompt loan creation if loan_id was not given
    # TODO: request email confirmation if email was given
    return Response(json.dumps(result, default=str), mimetype='application/json')


@app.route('/coops', methods=['GET'])
@jwt_required
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


@app.route('/loans', methods=['GET'])
@jwt_required
def loans():
  loans = Loan.query.all()
  data = []
  for loan in loans:
    user = User.query.filter(loan.user_id == User.id).first()
    data.append(
      {
        'name': user.first_name + ' ' + user.last_name,
        'start': loan.loan_start,
        'end': loan.loan_end,
        'interest': loan.interest,
        'initial': loan.initial_balance,
        'remaining': loan.balance
      }
    )
  results = {'data': data}
  return Response(json.dumps(results), mimetype='application/json')


@app.route('/register', methods=['POST'])
def register():
  email = request.form['email']
  test = User.query.filter_by(email=email).first()
  if test:
    return Response(json.dumps({'message': 'That email already exists.'}), mimetype='application/json'), 409
  else:
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    last_name = request.form['last_name']
    password = request.form['password']
    role_id = request.form['role_id']
    co_op_id = request.form['co_op_id']
    phone = request.form['phone']
    user = User(first_name=first_name, last_name=last_name, email=email, password=sha256.hash(password), role_id=role_id, co_op_id=co_op_id, phone=phone)
    db.session.add(user)
    db.session.commit()
    return Response(json.dumps({ 'message': 'Admin created successfully.' }), mimetype='application/json'), 201


@app.route('/login', methods=['POST'])
def login():
  if request.is_json:
    email = request.json['email']
    password = request.json['password']
  else:
    email = request.form['email']
    password = request.form['password']
  test = User.query.filter_by(email=email).first()
  if test:
    if sha256.verify(password, test.password):
      access_token = create_access_token(identity=email)
      return Response(json.dumps({ 'message': 'Login succeeded', 'access_token': access_token }), mimetype='application/json')
    else:
      return Response(json.dumps({ 'message': 'Invalid email/password.' }), mimetype='application/json'), 401
  else:
    return Response(json.dumps({ 'message': 'That email does not exist.' }), mimetype='application/json'), 401


if __name__ == '__main__':
  app.run()