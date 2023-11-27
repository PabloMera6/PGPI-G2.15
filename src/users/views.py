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
            messages.success(request, f'Correo electrónico y contraseña son obligatorios.')
            return redirect('register')

        if UserProfile.objects.filter(email=email).exists():
            messages.success(request, f'El correo electrónico {email} ya está registrado.')
            return redirect('register')

        try:
            user = UserProfile.objects.create_user(email=email, password=password, full_name=full_name, phone=phone, address=address)
            return redirect('initial')
        except IntegrityError:
            messages.success(request, f'Ha ocurrido un error al crear un usuario.')
            return redirect('register')

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
            messages.success(request, f'Correo electrónico y contraseña son obligatorios.')
            return redirect('login')

        try:
            user = UserProfile.objects.get(email=email)
        except UserProfile.DoesNotExist:
            messages.success(request, f'El correo electrónico {email} no está registrado.')
            return redirect('login')

        if not user.check_password(password):
            messages.success(request, f'Contraseña incorrecta.')
            return redirect('login')

        user = authenticate(request, username=email, password=password)

        if user is not None and user.is_active:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
        else:
            messages.success(request, f'Su cuenta ha sido desactivada.')
            return redirect('login')
        return redirect('initial')


class UserProfileView(APIView):
    template_name = 'users/profile.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/')
        current_user = request.user
        return render(request, self.template_name, {'current_user': current_user})
    

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('/')

        full_name = request.data.get('full_name', '')
        phone = request.data.get('phone', '')
        address = request.data.get('address', '')
        new_email = request.data.get('email', '')

        try:
            user_profile = request.user
        except ObjectDoesNotExist:
            messages.success(request, f'El usuario no existe.')
            return redirect('profile')

        if new_email and UserProfile.objects.exclude(pk=user_profile.pk).filter(email=new_email).exists():
            messages.success(request, f'El correo electrónico {new_email} ya está registrado.')
            return redirect('profile')

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
            return redirect('/')
        current_user = request.user
        if current_user.is_staff:
            users = UserProfile.objects.all()
            return render(request, self.template_name, {'users': users})
        else:
            return redirect('/')
        
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

