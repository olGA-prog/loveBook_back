from django.urls import path
from . import views
from .views import create_payment, yookassa_webhook

urlpatterns = [

    path('users/<int:pk>/', views.CustomUserDetail.as_view(), name='users-detail'),
    path('create_payment/', create_payment, name='create_payment'),
    path('save_user/', save_user, name='save_user'),
]