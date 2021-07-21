""" The main Flask application file that bootstraps and starts the app. """

import os

from flask_jwt import JWT
from flask_restful import Api
from flask_cors import CORS
from security import authenticate, identity

from bootstrap import app_factory, database_factory
from resources.revolving_fund import RevolvingFund, RevolvingFundList
from resources.member import Member, NewMember, MemberList
from resources.co_op import CoOp, CoOpList
from resources.role import RoleList
from resources.transaction import Transaction, TransactionList
from resources.send import Send
from resources.message import Message

import seed_data

app = app_factory()
app.secret_key = 'very_secret_key'

CORS(app)
db = database_factory(app)

# Seed with sample data:
@app.before_first_request
def create_tables():
    seed_data.create_tables(db)

api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(RevolvingFund, '/revolving_funds/<string:revolving_fund_id>')
api.add_resource(RevolvingFundList, '/revolving_funds')

api.add_resource(Member, '/members/<string:member_id>')
api.add_resource(NewMember, '/members')
api.add_resource(MemberList, '/members')

api.add_resource(CoOp, '/co_ops/<string:co_op_id>')
api.add_resource(CoOpList, '/co_ops')

api.add_resource(RoleList, '/roles')

api.add_resource(Transaction, '/transactions/<string:transactions_id>')
api.add_resource(TransactionList, '/transactions')

api.add_resource(Send, '/send')

api.add_resource(Message, '/')

@app.route("/health-check")
def health_check():
    return {"success": True}


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG", False))
