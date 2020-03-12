from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    jwt_refresh_token_required, 
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
)
from models.user import UserModel
from blacklist import BLACKLIST

_user_paser = reqparse.RequestParser()
_user_paser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
_user_paser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

class UserRegister(Resource):

    def post(self):
        data = _user_paser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400
        
        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201

class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = _user_paser.parse_args()

        user = UserModel.find_by_username(data['username'])

        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True, expires_delta=False)
            refresh_token = create_refresh_token(user.id)
            
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {'message': 'Invalid credentials'}, 401

class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti'] # JWT ID
        BLACKLIST.add(jti)
        return {'message': 'Successfully logged out.'}, 200
