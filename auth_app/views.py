from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login , logout
from plagDetector.views import home 
from django.views.decorators.csrf import csrf_exempt
from .models import *

# Create your views here.
def logout_user(request):
    print("in logout")
    if request.user.is_authenticated:
        logout(request)
        return home(request)
@csrf_exempt
def login_user(request):
    if request.user.is_authenticated:
        print("bhsod")
        logout(request)
        return home(request)
    
    email = request.POST.get('email')
    password = request.POST.get('password')
    print(email , password)
    username = User.objects.get(email = email)
    #username = "u2"
    username = username.username
    print(username)
    user = authenticate(request ,username=username, password=password)
    if user is not None:
        print("user")
        login(request, user)
        return redirect('home')
    else:
        print("not")
        return HttpResponse("wrong email or password")