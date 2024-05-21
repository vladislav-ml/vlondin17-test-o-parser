from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers

from product.models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('name', 'price', 'description', 'image_url', 'discount')


class CountSerializer(serializers.Serializer):
    product_count = serializers.IntegerField(default=10, help_text='Допустимы значения от 1 до 50', initial=10, validators=[MinValueValidator(1), MaxValueValidator(50)])

    def create(self, validated_data):
        return
