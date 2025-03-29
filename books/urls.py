from django.urls import path, re_path
from . import views

urlpatterns = [

    path('categories/', views.CategoryList.as_view(), name='category-list'),


    path('authors/', views.AuthorList.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorDetail.as_view(), name='author-detail'),


    path('series/', views.SeriesList.as_view(), name='series-list'),
    path('series/<int:pk>/', views.SeriesDetail.as_view(), name='series-detail'),

    path('books/', views.BookList.as_view(), name='books-list'),
    path('books/<int:pk>/', views.BookDetail.as_view(), name='books-detail'),

    path('orders/<int:pk>/', views.OrderDetail.as_view(), name='orders-detail'),
    path('payments/<int:pk>/', views.PaymentDetail.as_view(), name='payments-detail'),

    path('categories/<int:category_id>/books/', views.BookListByCategory.as_view(), name='book-list-by-category'),
    path('authors/<int:author_id>/books/', views.BookListByAuthor.as_view(), name='book-list-by-author'),
    path('series/<int:series_id>/books/', views.BookListBySeries.as_view(), name='book-list-by-series'),
    path('orders/', views.OrderCreate.as_view(), name='order-create'),
]