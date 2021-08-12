from django.http import JsonResponse,HttpResponse
from django.shortcuts import render , redirect


#########################################################


def home(request):
    context = {'navigation': [1,2,3,4,5,6,7]}
    return render(request,'plagDetector/home.html',context)


def search(request):
    if request.method == 'POST':
        text1 = request.POST.get('text1', None)
        text2 = request.POST.get('text2', None)
        context = {'navigation': [text1,text2,'vau','pinu','nikhil']}
        return render(request,'plagDetector/home.html',context)
    else:
        return render(request,'plagDetector/home.html')