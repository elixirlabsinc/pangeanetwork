from app import create_app, db
import os
import os.path as op
from datetime import datetime
from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import Response
from app.models import User, CoOp, Role, Loan, Transaction 
import africastalking
import json

app = create_app()

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


# Routes
@app.route('/', methods=['POST'])
def index():
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


@app.route('/loans', methods=['GET'])
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