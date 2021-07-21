import os

from flask_restful import Resource, reqparse
import africastalking

class Send(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('message',
                        type=str,
                        required=True,
                        help="The message field cannot be left blank")
    parser.add_argument('phone_number',
                        type=str,
                        required=True,
                        help="The phone_number field cannot be left blank")

    username = "sandbox"
    api_key = os.environ.get('AT_API_KEY')
    africastalking.initialize(username, api_key)
    sms = africastalking.SMS

    def send_missing_user_error(self, sender_phone):
      error_text = self.sms.send(
        "The user you are trying to update does not exist in our database. Please text <ADD {user number}> if you would like to add them", ['+' + str(sender_phone)])
      print(error_text)
      return 'error: user does not exist'
      
    @classmethod
    def post(cls, message, phone_number):
        try:
            response = cls.sms.send(message, [phone_number])
            print(response)
        except Exception as e:
            print('Encountered an error while sending: %s' % str(e))
            response = 'Encountered an error while sending: %s' % str(e)

        return {"result": response}


