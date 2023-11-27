from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .models import UserProfile
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib import messages



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

        if UserProfile.objects.filter(email=email).exists():
            return Response({'error': 'El correo electrónico ya está en uso.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserProfile.objects.create_user(email=email, password=password, full_name=full_name, phone=phone, address=address)
            return redirect('initial')
        except IntegrityError:
            return Response({'error': 'Ha ocurrido un error al crear el usuario.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return redirect('initial')

class LoginView(APIView):
    def get(self, request):
        return render(request, 'users/login.html')

    def post(self, request):
        email = request.data.get('email', '')
        password = request.data.get('password', '')

        if not email or not password:
            return Response({'error': 'Correo electrónico y contraseña son obligatorios.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserProfile.objects.get(email=email)
        except UserProfile.DoesNotExist:
            return Response({'error': 'El correo electrónico no existe.'}, status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            return Response({'error': 'Contraseña incorrecta.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=email, password=password)

        if user is not None and user.is_active:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
        else:
            return Response({'error': 'Su cuenta ha sido dada de baja por un administrador.'}, status=status.HTTP_400_BAD_REQUEST)
        return redirect('initial')


class UserProfileView(APIView):
    template_name = 'users/profile.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Acceso denegado. Debes iniciar sesión para ver este contenido.")
        current_user = request.user  # Obtén el UserProfile del usuario actual
        return render(request, self.template_name, {'current_user': current_user})
    

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Acceso denegado. Debes iniciar sesión para actualizar tu perfil.'}, status=status.HTTP_403_FORBIDDEN)

        full_name = request.data.get('full_name', '')
        phone = request.data.get('phone', '')
        address = request.data.get('address', '')
        new_email = request.data.get('email', '')

        try:
            user_profile = request.user
        except ObjectDoesNotExist:
            return Response({'error': 'UserProfile no encontrado para este usuario.'}, status=status.HTTP_404_NOT_FOUND)

        if new_email and UserProfile.objects.exclude(pk=user_profile.pk).filter(email=new_email).exists():
            return Response({'error': 'El nuevo correo electrónico ya está en uso.'}, status=status.HTTP_400_BAD_REQUEST)

        user_profile.full_name = full_name
        user_profile.phone = phone
        user_profile.address = address

        if new_email:
            user_profile.email = new_email

        user_profile.save()
        return redirect('initial')

class ListUsersView(APIView):
    template_name = 'users/administrate_users.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Acceso denegado. Debes iniciar sesión para ver este contenido.")
        current_user = request.user
        if current_user.is_staff:
            users = UserProfile.objects.all()
            return render(request, self.template_name, {'users': users})
        else:
            return HttpResponseForbidden("Acceso denegado. Debes iniciar sesión para ver este contenido.")
        
    def post(self, request):
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')

        user = UserProfile.objects.get(id=user_id)

        if action == 'activate':
            user.is_active = True
            user.save()
            messages.success(request, f'El usuario {user.email} ha sido dado de alta.')
        elif action == 'deactivate':
            user.is_active = False
            user.save()
            Token.objects.filter(user=user).delete()
            messages.success(request, f'El usuario {user.email} ha sido dado de baja.')

        return redirect(reverse('administrate_users'))

