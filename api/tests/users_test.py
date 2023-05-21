import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from ..model.users import User


class UserTestCase(unittest.TestCase):
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

    def test_user_registration(self):
        data = {
            "username": "kelechi",
            "email": "this@gmail.com",
            "password": "password"
        }
        response = self.client.post('/auth/signup', json=data)
        user = User.query.filter_by(email="this@gmail.com").first()
        assert user.email == "this@gmail.com"
        assert response.status_code == 201

    def test_user_login(self):
        data = {
            "email": "this@gmail.com",
            "password": "password"
        }

        response = self.client.post('/auth/login', json=data)
        assert response.status_code == 400
