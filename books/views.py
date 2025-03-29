from django.shortcuts import render

from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Author, Series, Book, Order, OrderItem, Payment
from .serializers import CategorySerializer, AuthorSerializer, SeriesSerializer, BookSerializer, OrderSerializer, OrderItemSerializer, PaymentSerializer
from rest_framework.permissions import IsAuthenticated

import os
from django.http import FileResponse, Http404
from django.conf import settings

class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# Author Views (for ListAPIView and RetrieveAPIView)
class AuthorList(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class AuthorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


# Series Views (for ListAPIView and RetrieveAPIView)
class SeriesList(generics.ListCreateAPIView):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer


class SeriesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer


# Book Views (for ListAPIView and RetrieveAPIView)
class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# Order Views (for RetrieveAPIView)
class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


# Payment Views (for RetrieveAPIView)
class PaymentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class BookListByCategory(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Book.objects.filter(category_id=category_id)  # Assuming Book has a ForeignKey to Category

class BookListByAuthor(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        author_id = self.kwargs['author_id']
        return Book.objects.filter(author_id=author_id)  # Assuming Book has a ForeignKey to Author

class BookListBySeries(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        series_id = self.kwargs['series_id']
        return Book.objects.filter(series_id=series_id)  # Assuming Book has a ForeignKey to Series


class OrderCreate(generics.CreateAPIView):
    serializer_class = OrderSerializer


    def create(self, request, *args, **kwargs):
        order_items_data = request.data.pop('items', [])

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save(user=request.user)

        total_amount = 0.0

        for item_data in order_items_data:
            item_data['order'] = order.id
            item_serializer = OrderItemSerializer(data=item_data)
            item_serializer.is_valid(raise_exception=True)
            order_item = item_serializer.save()
            total_amount += order_item.quantity * order_item.book.price

        order.total_amount = total_amount
        order.save()

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

def serve_ebook(request, filename):
    file_path = os.path.join(settings.BASE_DIR, 'books', 'ebooks', filename)

    try:
        with open(file_path, 'rb') as ebook:  # Open in binary read mode
            return FileResponse(ebook, as_attachment=True, filename=filename) # Django built in class
    except FileNotFoundError:
        raise Http404("Ebook not found")