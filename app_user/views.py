import json

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import yookassa
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework.permissions import IsAuthenticated

class CustomUserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def post(self, request, *args, **kwargs):
        telegram_id = request.data.get('telegram_id')

        if not telegram_id:
            return Response({"error": "telegram_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(telegram_id=telegram_id)
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            # User does not exist, create a new user
            # Ensure that telegram_id is included in the data for the serializer
            user_data = request.data.copy()  # Create a mutable copy of the data
            user_data['telegram_id'] = telegram_id  # Ensure telegram_id is included

            serializer = self.get_serializer(data=user_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def save_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            username = data.get('username', '')
            first_name = data.get('first_name', '')
            last_name = data.get('last_name', '')

            user, created = CustomUser.objects.update_or_create(
                telegram_id=user_id,
                defaults={
                    'username': username,
                    'first_name': first_name,
                    'last_name': last_name
                    # Другие поля можно оставить по умолчанию
                }
            )
            return JsonResponse({
                'status': 'success',
                'user_id': user.user_id,
                'created': created
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def create_payment(request):
    if request.method == 'POST':
        yookassa.configuration.account_id = "YOUR_SHOP_ID"
        yookassa.configuration.secret_key = "YOUR_SECRET_KEY"

        payment = yookassa.Payment.create({
            "amount": {
                "value": request.POST.get('amount'), # Get the amount from the client request
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://yourwebsite.com/success"  # Replace with your actual success URL
            },
            "capture": True,  # Automatically capture the payment
            "description": "Payment for book"
        })
        return JsonResponse({'confirmation_url': payment.confirmation.confirmation_url})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

# Example (receiving webhook)
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def yookassa_webhook(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        paymentId = data['object']['id']
        print(paymentId)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=405)