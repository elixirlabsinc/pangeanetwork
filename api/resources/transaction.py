from flask_restful import Resource
from models.transaction import TransactionModel


class Transaction(Resource):
    def get(self, transaction_id):
        transaction = TransactionModel.find_by_id(transaction_id)
        if transaction:
            return transaction.json()
        return {'message': 'Transaction not found'}, 400


class TransactionList(Resource):
    def get(self):
        transactions = TransactionModel.query.all()

        return {'transactions': [transaction.json() for transaction in transactions]}
