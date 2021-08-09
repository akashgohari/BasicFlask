import hmac

from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jti, \
    get_jwt
from flask_restful import Resource, reqparse

from blacklist import BLACKLIST
from models.user import UserModel

_user_parser = reqparse.RequestParser()
_user_parser.add_argument("username", type=str, required=True)
_user_parser.add_argument("password", type=str, required=True)


class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data["username"])
        if user and hmac.compare_digest(user.password, data["password"]):
            return {
                "access_token": create_access_token(identity=user.id, fresh=True),
                "refresh_token": create_refresh_token(user.id),
            }
        return {"message": "Invalid Credential"}, 401


class UserRegister(Resource):
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data["username"])
        if user:
            return {"message": "User already exists"}, 400
        user = UserModel(**data)
        user.add_update_user()
        return {"message": "Successfully added user"}, 201


class User(Resource):
    @classmethod
    def get(cls, name):
        user = UserModel.find_by_username(name)
        if user:
            return {'user': user.to_json}
        return {"message": "User does not exists"}


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        return {"access_token": create_access_token(identity=current_user, fresh=False)}


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        access_id = get_jwt()['jti']
        BLACKLIST.add(access_id)
