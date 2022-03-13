from django.db.models import fields
from rest_framework import serializers
from .models import UpdateProductModel, AddProductModel


class UpdateProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpdateProductModel
        fields = (
        'yotpo_id', 'external_id', 'product_title', 'product_url', 'product_image_url', 'product_price', 'product_currency', 'upc', 'mpn', 'brand', 'isbn', 'sku', 'product_tags', 'blacklisted', 'product_group',)

class AddProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddProductModel
        fields = (
        'external_id', 'product_title', 'description', 'product_url', 'product_price', 'sku',)
