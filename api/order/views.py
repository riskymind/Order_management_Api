from flask_restx import Namespace, Resource, fields
from ..model.orders import Order
from ..model.users import User
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..utils import db

order_namespace = Namespace('order', description='Order namespace')

order_model = order_namespace.model(
    'Order', {
        'size': fields.String(description='order size', required=True,
                              enum=['SMALL', 'MEDIUM', 'LARGE', 'EXTRA_LARGE']),
        'order_status': fields.String(description='order status', required=True,
                                      enum=['PENDING', 'IN_TRANSIT', 'DELIVERED']),
        'flavour': fields.String(description='flavour')
    }
)

order_response_model = order_namespace.model(
    'Orders', {
        'id': fields.Integer(description='order id'),
        'size': fields.String(description='order size', required=True,
                              enum=['SMALL', 'MEDIUM', 'LARGE', 'EXTRA_LARGE']),
        'order_status': fields.String(description='order status', required=True,
                                      enum=['PENDING', 'IN_TRANSIT', 'DELIVERED']),
        'flavour': fields.String(description='flavour')
    }
)


@order_namespace.route('/orders')
class PlaceOrGetOrder(Resource):

    @order_namespace.marshal_list_with(order_response_model)
    @jwt_required()
    def get(self):
        """
        Get Orders
        :return:
        """
        orders = Order.query.all()
        return orders, HTTPStatus.OK

    @order_namespace.expect(order_model)
    @order_namespace.marshal_with(order_response_model)
    @jwt_required()
    def post(self):
        """
        Place Orders
        :return:
        """
        user_email = get_jwt_identity()
        current_user = User.query.filter_by(email=user_email).first()
        data = order_namespace.payload
        new_order = Order(
            size=data['size'],
            quantity=data['quantity'],
            flavour=data['flavour']
        )

        new_order.customer = current_user
        new_order.save()
        return new_order, HTTPStatus.CREATED


@order_namespace.route('/<int:order_id>')
class GetUpdateOrDeleteOrder(Resource):

    @order_namespace.marshal_with(order_response_model)
    @jwt_required()
    def get(self, order_id: int):
        """
        Get order via ID
        :param order_id:
        :return:
        """
        order = Order.get_by_id(order_id)
        return order, HTTPStatus.OK

    @order_namespace.marshal_with(order_response_model)
    @order_namespace.expect(order_model)
    @jwt_required()
    def put(self, order_id):
        """
        Update an order
        :param order_id:
        :return:
        """
        order_to_update = Order.get_by_id(order_id)
        data = order_namespace.payload
        order_to_update.quantity = data['quantity']
        order_to_update.size = data['size']
        order_to_update.flavour = data['flavour']
        db.session.commit()
        return order_to_update, HTTPStatus.OK

    @order_namespace.marshal_with(order_response_model)
    @jwt_required()
    def delete(self, order_id):
        """
        Delete Order
        :param order_id:
        :return:
        """
        order = Order.get_by_id(order_id)
        order.delete()
        return order, HTTPStatus.NO_CONTENT


@order_namespace.route('/user/<int:user_id>/order/<int:order_id>')
class GetUserOrder(Resource):
    @order_namespace.marshal_with(order_response_model)
    @jwt_required()
    def get(self, user_id: int, order_id: int):
        """
        Get user order
        :param user_id:
        :param order_id:
        :return:
        """
        user = User.get_by_id(user_id)
        order = Order.query.filter_by(id=order_id).filter_by(user=user).first()
        return order, HTTPStatus.OK


@order_namespace.route('/user/<int:user_id>/orders')
class UserOrders(Resource):
    @order_namespace.marshal_list_with(order_response_model)
    @jwt_required()
    def get(self, user_id: int):
        """
        Get User Orders
        :param user_id:
        :return:
        """
        user = User.get_by_id(user_id)
        orders = user.orders
        return orders, HTTPStatus.OK


@order_namespace.route('/order/status/<int:order_id>')
class UpdateOrderStatus(Resource):
    @order_namespace.expect(order_model)
    @order_namespace.marshal_with(order_response_model)
    @jwt_required()
    def patch(self, order_id: int):
        """
        Update Order status
        :param order_id:
        :return:
        """
        data = order_namespace.payload
        order = Order.get_by_id(order_id)
        order.order_status = data['order_status']
        db.session.commit()
        return order, HTTPStatus.OK
