from flask import Flask
from flask_restx import Api
from .auth.views import auth_namespace
from .order.views import order_namespace
from .config.config import config_dict
from .utils import db
from .model.orders import Order
from .model.users import User
from flask_migrate import Migrate


def create_app(config=config_dict['dev']):
    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)

    migrate = Migrate(app, db)

    api = Api(app)

    api.add_namespace(auth_namespace, path='/auth')
    api.add_namespace(order_namespace, path='/order')

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': User,
            'Order': Order
        }

    return app
