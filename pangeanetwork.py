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
from flask import Flask
from flask_mail import Mail
from flask_mail import Message
from flask_bcrypt import Bcrypt
import random
import string


app = create_app()

bcrypt = Bcrypt(app)

username = "sandbox"
api_key = os.environ.get('AT_API_KEY')
test_number = "+254456923994"
africastalking.initialize(username, api_key)
sms = africastalking.SMS

# initialize mail app
mail = Mail()

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

def send_not_officer_error(sender_phone):
    error_text = sms.send(
            "The user, {user number}, you have specified does not have the required role of officer in order to complete the transaction.", ['+' + str(sender_phone)]) 
    print(error_text) 
    return 'error: user not an officer'

def confirm_transaction(from_user, msg):
  officer_role = Role.query.filter(Role.name == 'officer').first()
  officer = User.query.filter(User.phone == int(from_user), User.role_id == officer_role.id).first() 
  if officer is None: 
      return send_not_officer_error(from_user) 
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
  # create password hash
  pw_hash = bcrypt.generate_password_hash(user_data['password'])

  new_user = User(
    first_name=user_data['first_name'],
    last_name=user_data['last_name'],
    email=user_data['email'],
    phone=user_data['phone'],
    active=True,
    password=pw_hash,
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


@app.route('/coops', methods=['GET', 'PUT'])
def coops():
  '''
  GET: queries for all coops
  PUT: updates an existing coop based on the name
    Json data:
      name (str): the name of the coop
      start_date (str): the start date of the coop
      end_date (str): the end date of the coop
      location (str): the location of the coop
      interest (float): the interest of the coop
      intial_balance (float): the initial balance of the coop
      current_balance (float): the current balance of the coop
      expected_repayment (str): the expected repayment of the coop
  '''

  data = []
  coops = CoOp.query.all()

  if(request.method == 'GET'):

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
  
  elif(request.method == 'PUT'):
    content = request.json
    results = {}
    isCoopExist = False


    for coop in coops:
      if(content['name'] == coop.name):
        coop.name = content['name']
        coop.start_date = content['start_date']
        coop.end_date = content['end_date']
        coop.location = content['location']
        coop.initial_balance = content['initial_balance']
        coop.current_balance = content['current_balance']
        coop.expected_repayment = content['expected_repayment']
        
        db.session.commit()

        isCoopExist = True

        results = {"code": 200, "status": "ok"}
        return Response(json.dumps(results), mimetype='application/json')

    if(isCoopExist == False):
        results = {"code": 404, "status": "coop not found"}
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

@app.route('/loan/<loanid>', methods=['GET'])
def loan(loanid):
  loanid = int(loanid)
  loan = Loan.query.filter(loanid == Loan.id).first()
  if(loan):
    user = User.query.filter(loan.user_id == User.id).first()
    data = []
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
    results = {'data': data, 'code': 200, 'status': 'ok'}
    return Response(json.dumps(results), mimetype='application/json')
  else:
    results = {'code':404, 'status': 'loan not found'}
    return Response(json.dumps(results), mimetype='application/json')

@app.route('/forgotpassword', methods=['POST'])
def forgotPassword():
  '''
  Fill in sender email fields
  '''
  body = request.json
  encoded_jwt = jwt.encode({'payload': body['email']}, 'elixir', algorithm='HS256')
  port = 587 
  smtp_server = "smtp.gmail.com"
  msg = MIMEMultipart("alternative")
  msg['Subject'] = "Pangea Network Password Reset"
  msg['From'] = ''
  msg['To'] = body['email']
  html = """\
  Hello this is your password reset token<br/>
  """
  html += str(encoded_jwt)
  msg.attach(MIMEText(html, 'html'))
  context = ssl.create_default_context()

  server = smtplib.SMTP(smtp_server, port)
  server.ehlo() 
  server.starttls(context=context)
  # server.ehlo()
  server.login(msg['From'],'')
  server.sendmail(msg['From'],msg['To'],msg.as_string())
  server.close()

  return Response(json.dumps({'status':'ok', 'email': body['email']}),mimetype='application/json')

@app.route('/passwordreset', methods=['POST'])
def passwordReset():
  '''
  Updates user's password based on json data sent from the client

    Json data:
      email (str): the email of the user
      password (str): the password of the user
  '''
  content = request.json

  data = []
  users = User.query.all()

  for user in users:
    if(user.email == content['email']):
      # hash password
      pw_hash = bcrypt.generate_password_hash(content['password'])
      user.password = pw_hash

  db.session.commit()

  results = {"code": 200, "status": "ok"}

  return Response(json.dumps(results, default=str), mimetype='application/json')
   

if __name__ == '__main__':
  app.run()
