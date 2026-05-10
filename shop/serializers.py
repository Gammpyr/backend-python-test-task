from rest_framework import serializers
from .models import Category, Product, Cart, CartItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image', 'subcategory']
        read_only_field = ['id', ]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'image', 'price', 'category', 'created_at', 'image_small', 'image_medium',
                  'image_large']
        read_only_fields = ['id', 'created_at', 'image_small', 'image_medium', 'image_large']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(subcategory__isnull=False)


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'updated_at', ]
        read_only_field = ['id', 'created_at', 'updated_at', ]


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'cart_id', 'product_id', 'quantity', ]
        read_only_field = ['id', ]
