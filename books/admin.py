from django.contrib import admin
from .models import Category, Author, Series, Book, Order, OrderItem, Payment

admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Series)
admin.site.register(Book)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
