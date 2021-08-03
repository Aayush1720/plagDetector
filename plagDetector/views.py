from django.http import JsonResponse
from django.shortcuts import render , redirect


#########################################################


def home(request):
    context = {}
    return render(request,'plagDetector/home.html',context)