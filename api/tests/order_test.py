import unittest
from .. import create_app
from ..utils import db
from ..config.config import config_dict
from flask_jwt_extended import create_access_token
from ..model.orders import Order


class OrderTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config=config_dict['test'])
        self.appctx = self.app.app_context()
        self.appctx.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.drop_all()
        self.appctx.pop()
        self.app = None
        self.client = None

    def test_get_all_order(self):
        token = create_access_token(identity="this@gmail.com")
        headers = {"Authorization": f"Bearer {token}"}
        response = self.client.get("/order/orders", headers=headers)
        assert response.status_code == 200

    def test_create_order(self):
        data = {
            "size": "LARGE",
            "quantity": 2,
            "flavour": "choco"
        }

        token = create_access_token(identity="this@gmail.com")
        headers = {"Authorization": f"Bearer {token}"}
        response = self.client.post("/order/orders", json=data, headers=headers)
        assert response.status_code == 201
        orders = Order.query.all()
        assert len(orders) == 1


