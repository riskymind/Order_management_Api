from flask import Flask
from flask_restx import Api
from .auth.views import auth_namespace
from .order.views import order_name


def create_app():
    app=Flask(__name__)

    api=Api(app)

    api.add_namespace(auth_namespace)
    api.add_namespace(order_name)

    return app
