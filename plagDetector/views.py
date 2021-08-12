from django.http import JsonResponse,HttpResponse
from django.shortcuts import render , redirect
import nltk
#########################################################


def home(request):
    context = {'navigation': [1,2,3,4,5,6,7]}
    return render(request,'plagDetector/home.html',context)


def plag(text1,text2):
    str1 = ''.join(text1)
    str2 = ''.join(text2)
    sent_text1 = str1.split('.')
    sent_text2 = str2.split('.')

    final_list = []
    for z in sent_text1:
        #print(z)
        for y in sent_text2:
            if z==y:
                final_list.append(z)
    
    return final_list

def search(request):
    if request.method == 'POST':
        text1 = request.POST.get('text1', None)
        text2 = request.POST.get('text2', None)
        final_list = plag(text1,text2)
        context = {'navigation': final_list}
        return render(request,'plagDetector/home.html',context)
    else:
        return render(request,'plagDetector/home.html')