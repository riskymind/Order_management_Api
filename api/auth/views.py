from flask_restx import Namespace, Resource, fields
from flask import request
from ..model.users import User
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus

auth_namespace = Namespace('auth', description='authentication namespace')

signup_model = auth_namespace.model(
    'SignUp', {
        'id': fields.Integer(),
        'username': fields.String(required=True, description='User name'),
        'email': fields.String(required=True, description='User email'),
        'password': fields.String(required=True, description='User password')
    }
)

user_model = auth_namespace.model(
    'User', {
        'id': fields.Integer(),
        'username': fields.String(required=True, description='User name'),
        'email': fields.String(required=True, description='User email'),
        'password_hash': fields.String(required=True, description='User password'),
        'is_active': fields.Boolean(description="This shows that User is active"),
        'is_staff': fields.Boolean(description="This shows of use is staff")
    }
)


@auth_namespace.route('/signup')
class SignUp(Resource):
    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(user_model)
    def post(self):
        """
        Sign up users
        """
        data = request.get_json()

        new_user = User(
            username=data.get('username'),
            email=data.get('email'),
            password_hash=generate_password_hash(data.get('password'))
        )

        new_user.save()

        return new_user, HTTPStatus.CREATED


@auth_namespace.route('/login')
class Login(Resource):
    def post(self):
        """
        Login in user and generate jwt
        """
        pass
