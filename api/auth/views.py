from flask_restx import Namespace, Resource, fields
from flask import request
from ..model.users import User
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import BadRequest, Conflict
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

auth_namespace = Namespace('auth', description='authentication namespace')

signup_model = auth_namespace.model(
    'SignUp', {
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

login_model = auth_namespace.model(
    'Login', {
        'email': fields.String(required=True, description='User email'),
        'password': fields.String(required=True, description='User password')
    }
)


@auth_namespace.route('/signup')
class SignUp(Resource):
    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(user_model)
    @auth_namespace.doc(
        description='Sign up user'
    )
    def post(self):
        """
        Sign up users
        """
        data = request.get_json()
        # data = auth_namespace.payload
        # try:
        new_user = User(
            username=data.get('username'),
            email=data.get('email'),
            password_hash=generate_password_hash(data.get('password'))
        )

        new_user.save()

        return new_user, HTTPStatus.CREATED
    # except Exception as e:
    # raise Conflict(f"User with email {data.get('email')} exists")


@auth_namespace.route('/login')
class Login(Resource):
    @auth_namespace.expect(login_model)
    @auth_namespace.doc(
        description='Login user'
    )
    def post(self):
        """
        Login in user and generate jwt
        """
        # data = request.get_json()
        data = auth_namespace.payload
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()

        if (user is not None) and check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=user.email)
            refresh_token = create_refresh_token(identity=user.email)

            response = {
                'message': 'Success',
                'access_token': access_token,
                'refresh_token': refresh_token
            }

            return response, HTTPStatus.OK
        raise BadRequest("Invalid Username or Password")


@auth_namespace.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        email = get_jwt_identity()

        access_token = create_access_token(identity=email)
        return {'message': 'Success', 'access_token': access_token}
