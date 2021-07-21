from flask_restful import Resource
from models.role import RoleModel


class Role(Resource):
    def get(self, role_id):
        role = RoleModel.find_by_id(role_id)
        if role:
            return role.json()
        return {'message': 'role not found'}, 400


class RoleList(Resource):
    def get(self):
        roles = RoleModel.query.all()

        return {'roles': [role.json() for role in roles]}
