from rest_framework import serializers
from .models import Category, Author, Series, Book, Order, OrderItem, Payment

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class SeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    category_ids = serializers.SerializerMethodField()  # New field for category IDs

    class Meta:
        model = Book
        fields = '__all__'  # Include 'category_ids' in the fields

    def get_category_ids(self, obj):
        # Return a list of category IDs for the book
        return [category.id for category in obj.categories.all()]

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)  # Nested serializer
    class Meta:
        model = Order
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'