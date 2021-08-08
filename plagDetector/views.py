from django.http import JsonResponse
from django.shortcuts import render , redirect


#########################################################


def home(request):
    context = {'navigation': [1,2,3,4,5,6,7]}
    return render(request,'plagDetector/home.html',context)