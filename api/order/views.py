from flask_restx import Namespace, Resource

order_name = Namespace('order', description='Order namespace')


@order_name.route('/')
class HelloOrder(Resource):
    def get(self):
        return {'message': 'Hello from order'}
