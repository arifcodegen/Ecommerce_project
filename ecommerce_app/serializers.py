from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    price = serializers.FloatField(write_only=True)  # For incoming data
    decrypted_price = serializers.FloatField(source='get_price', read_only=True)  # For outgoing data

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'decrypted_price', 'category']

    def create(self, validated_data):
        price = validated_data.pop('price')
        product = Product(**validated_data)
        product.set_price(price)
        product.save()
        return product

    def update(self, instance, validated_data):
        price = validated_data.pop('price', None)
        if price is not None:
            instance.set_price(price)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        return instance
