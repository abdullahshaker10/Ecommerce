from rest_framework import serializers
from .models import Order, OrderItem


class OrderSerializer(serializers.ModelSerializer):
    cart_total = serializers.SerializerMethodField('get_cart_items')

    def get_cart_items(self, Order):
        order_items = Order.orderitem_set.all()
        total = sum([item.quantity for item in order_items])
        return total

    class Meta:
        model = Order
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = '__all__'
