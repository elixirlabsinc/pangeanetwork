from flask_restful import Resource
from flask import request
from models.co_op import CoOpModel


class CoOp(Resource):
    def get(self, co_op_id):
        co_op = CoOpModel.find_by_id(co_op_id)
        if co_op:
            return co_op.json()
        return {'message': 'CoOp not found'}, 400


class CoOpList(Resource):
    def get(self):
        search = request.args.get('search')

        if search:
            co_ops = CoOpModel.query.filter(CoOpModel.name.ilike(f'%{search}%')).all()
        else:
            co_ops = CoOpModel.query.all()

        return {'co_ops': [co_op.json() for co_op in co_ops]}