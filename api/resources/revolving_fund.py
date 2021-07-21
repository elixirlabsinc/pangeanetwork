from flask_restful import Resource
from flask import request
from models.revolving_fund import RevolvingFundModel


class RevolvingFund(Resource):
    def get(self, revolving_fund_id):
        revolving_fund = RevolvingFundModel.find_by_id(revolving_fund_id)
        if revolving_fund:
            return revolving_fund.json()
        return {'message': 'Revolving Fund not found'}, 400


class RevolvingFundList(Resource):
    def get(self):
        revolving_funds = RevolvingFundModel.query.all()

        return {'revolving_funds': [revolving_fund.json() for revolving_fund in revolving_funds]}
