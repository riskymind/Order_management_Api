from flask import Flask
from flask_restx import Api
from .auth.views import auth_namespace
from .order.views import order_namespace
from .config.config import config_dict
from .utils import db
from .model.orders import Order
from .model.users import User
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound, MethodNotAllowed


def create_app(config=config_dict['dev']):
    app = Flask(__name__)

    app.config.from_object(config)

    authorization = {
        "Bearer auth": {
            'type': "apiKey",
            'in': 'header',
            'name': "Authorization",
            'description': "Add a JWT with ** Bearer &lt;JWT&gt; to authorize"
        }
    }

    api = Api(
        app,
        title="Order management Api",
        description="A REST API for a Order Management service",
        authorizations= authorization,
        security="Bearer Auth"
    )

    api.add_namespace(auth_namespace, path='/auth')
    api.add_namespace(order_namespace, path='/order')

    db.init_app(app)
    jwt = JWTManager(app)
    migrate = Migrate(app, db)

    @api.errorhandler(NotFound)
    def not_found(error):
        return {"error": "Not Found"}, 404

    @api.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {"message": "Method not allowed"}, 405

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': User,
            'Order': Order
        }

    return app
