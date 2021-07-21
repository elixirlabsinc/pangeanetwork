from flask_jwt import jwt_required
from flask_restful import reqparse, Resource

from models.user import User


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank")

    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank")

    @jwt_required()
    def post(self):
        data = self.parser.parse_args()
        User(username=data["username"], password=data["password"])
        return {"message": "User created successfully."}, 201
