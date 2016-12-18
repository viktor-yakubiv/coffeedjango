from rest_framework import serializers
from .models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image']


class ToppingSerializer(serializers.HyperlinkedModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Topping
        fields = ['product']


class DrinkSerializer(serializers.HyperlinkedModelSerializer):
    product = ProductSerializer()
    toppings = ToppingSerializer(many=True)

    class Meta:
        model = Drink
        fields = ['product', 'toppings']


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'total']
