from flask_restx import Namespace, Resource

order_namespace = Namespace('order', description='Order namespace')


@order_namespace.route('/orders')
class PlaceOrGetOrder(Resource):
    def get(self):
        """
        Get Orders
        :return:
        """
        pass

    def post(self):
        """
        Place Orders
        :return:
        """
        pass


@order_namespace.route('/<int:order_id>')
class GetUpdateOrDeleteOrder(Resource):
    def get(self, order_id: int):
        """
        Get order via ID
        :param order_id:
        :return:
        """
        pass

    def put(self, order_id):
        """
        Update an order
        :param order_id:
        :return:
        """
        pass

    def delete(self, order_id):
        """
        Delete Order
        :param order_id:
        :return:
        """
        pass


@order_namespace.route('/user/<int:user_id>/order/<int:order_id>')
class GetUserOrder(Resource):
    def get(self, user_id: int, order_id: int):
        """
        Get user order
        :param user_id:
        :param order_id:
        :return:
        """
        pass


@order_namespace.route('/user/<int:user_id>/orders')
class UserOrders(Resource):
    def get(self, user_id: int):
        """
        Get User Orders
        :param user_id:
        :return:
        """
        pass


@order_namespace.route('/order/status/<int:order_id>')
class UpdateOrderStatus(Resource):
    def patch(self, order_id:int):
        """
        Update Order status
        :param order_id:
        :return:
        """
        pass