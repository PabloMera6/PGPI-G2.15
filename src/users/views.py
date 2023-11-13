from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .models import UserProfile
from django.shortcuts import render

class RegisterView(APIView):
    def get(self, request):
        return render(request, 'users/register.html')

    def post(self, request):
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        full_name = request.data.get('full_name', '')
        phone = request.data.get('phone', '')
        address = request.data.get('address', '')

        if not email or not password:
            return Response({'error': 'Correo electrónico y contraseña son obligatorios.'}, status=status.HTTP_400_BAD_REQUEST)
        
        User = get_user_model()
        if User.objects.filter(email=email).exists():
            return Response({'error': 'El correo electrónico ya está en uso.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create(email=email)
            user.set_password(password)
            user.save()

            UserProfile.objects.create(user=user, full_name=full_name, phone=phone, address=address)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'user_pk': user.pk, 'token': token.key}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'error': 'Ha ocurrido un error al crear el usuario.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
