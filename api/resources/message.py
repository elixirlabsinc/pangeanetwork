import os

from flask_restful import Resource, reqparse
from models.co_op import CoOpModel
from models.role import RoleModel
from models.transaction import TransactionModel
from models.user import UserModel
from resources.send import Send
from datetime import datetime

class Message(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('from', type=str, required=True)
    parser.add_argument('text', type=str, required=True)

    def add_transaction(self, from_user, msg):
      from_phone = int(from_user)
      print(from_phone)
      member_id = msg[1]
      member = UserModel.find_by_id(member_id)
      if member == None:
        return Send.send_missing_user_error(from_phone)
      amount = int(msg[2])
      if member.revolving_fund == None:
        officer_text = Send.post('ERROR: Given member does not have a current revolving_fund', [from_phone])
        print(officer_text)
        return 'Error: Member does not have a current revolving_fund'
      revolving_fund = member.revolving_fund
      new_user_transaction = TransactionModel(
        revolving_fund_id=member.revolving_fund.id,
        amount=amount,
        previous_balance=revolving_fund.balance,
        new_balance=revolving_fund.balance - amount,
        state='initiated',
        user_id=member.id,
        timestamp=datetime.now()
      )

      new_user_transaction.save_to_db()
      officer_role = RoleModel.find_by_name('Admin')
      co_op_officer = UserModel.query.filter(UserModel.role_id == officer_role.id, UserModel.co_op_id == member.co_op_id).first()
      
      try:
        response_text = Send.post("Transaction added. Requesting confirmation from Co-Op Leader", ['+' + str(from_phone)])
        leader_text = Send.post("A new repayment transaction has been added for member " + str(member.first_name) + " (ID: " + str(member.id) + ") in the amount of " + str(amount) + ". \
        Please respond with 'Y " + str(member.id) + "' to confirm this transaction is accurate or 'N " + str(member.id) + "' to reject it. Their new balance will be: " + 
        str(revolving_fund.balance - amount), ['+' + co_op_officer.phone])
        print(response_text)
        print(leader_text)
        return 'success: added loan transaction'
      except Exception as e:
        print('Encountered an error while sending: %s' % str(e))
        return 'Encountered an error while sending: %s' % str(e)

    
    def confirm_transaction(self, from_user, msg):
        officer = UserModel.find_by_phone(from_user)
        # TODO: return error message if user does not exist
        # TODO: return error message if user is not an officer
        member_id = msg[1]
        co_op = CoOpModel.find_by_co_op_id(officer.co_op_id)
        member = UserModel.find_by_member_and_co_op_id(member_id, co_op.id)
        if member == None:
          return Send.send_missing_user_error(from_user)
        if member.transactions == None:
          error_text = Send.post('ERROR: There is no transaction available to confirm for user ' + str(member.first_name) + '' + str(member.last_name), from_user)
          print(error_text)
          return 'error: transaction does not exist'
        else:
          user_transaction = member.transactions.all()[-1]
          if user_transaction.state == 'initiated':
            user_transaction.state = 'confirmed'
            member.loan.balance = user_transaction.new_balance
            co_op.current_balance -= user_transaction.amount
            member.save_to_db()
            co_op.save_to_db()
            user_transaction.save_to_db()
            try:
              officer_text = Send.post("Transaction complete. New balance for member " + str(member.id) + ' - ' + str(member.first_name) + " is " + str(member.loan.balance) + '. \
                New balance for Co-Op ' + co_op.name + ' is ' + str(co_op.current_balance), [from_user])
              if member.phone:
                member_text = Send.post('Transaction confirmed. Your new balance is ' + str(member.loan.balance), [member.phone])
                print(member_text)
              print(officer_text)
            except Exception as e:
              print('Encountered an error while sending: %s' % str(e))

    def get_members(self, from_user):
        user = UserModel.find_by_phone(from_user)
        if user == None:
          return "Error: you are not a registered user"
        if user.role.name != 'Admin':
          return "Error: you are not an officer"
        users = UserModel.find_all_members_by_co_op(user.co_op_id)
        members = 'Members in your coop:\n'
        for user in users:
          members += user.first_name + ' ' + user.last_name + ': (id = ' + str(user.id) + ')\n'
        return members


    def post(self):
        data = self.parser.parse_args()

        try:
          from_user = data['from']
        except:
          from_user = None
        if from_user == None:
          return 'failure: request error'
        msg = data['text'].split()
        cmd = msg[0].lower()
        if cmd == 'loan':
          if len(msg) != 3:
            return 'error'
          return self.add_transaction(from_user, msg)
        elif cmd == 'y':
          self.confirm_transaction(from_user, msg)
        elif cmd == 'n':
          return 'transaction denied'
          # TODO: remove transaction
        elif cmd == 'members':
          list_of_members = self.get_members(from_user)
          print(list_of_members)
          response = Send.post(list_of_members, from_user)
          return response
        # TODO: support 'new' command for new members and funds
        else:
          return 'error'
          # TODO: handle error
        return 'success'
