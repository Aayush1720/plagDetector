from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
import nltk
from .forms import UploadFileForm
from django.core.files.storage import FileSystemStorage
from auth_app.models import User

#########################################################


def home(request):
    context = {'navigation': []}
    is_authenticated = request.user.is_authenticated
    username = ""
    if is_authenticated:
        username = request.user.username 
    context = {'is_authenticated' : is_authenticated , 'username' : username }
    return render(request, 'plagDetector/home.html', context)


# test function to compare two texts -Tanmay/Aadarsh/Aayush
def plag(text1, text2):

    str1 = ''.join(text1)
    str2 = ''.join(text2)
    sent_text1 = str1.split('.')
    sent_text2 = str2.split('.')

    final_list = []  
    for z in sent_text1:
        # print(z)
        for y in sent_text2:
            if z == y:
                final_list.append(z)

    return final_list


# test function two check two input texts
def search(request):
    # search goes here
    if request.method == 'POST':
        text1 = request.POST.get('text1', None)
        text2 = request.POST.get('text2', None)
        final_list = plag(text1, text2)
        is_authenticated = request.user.is_authenticated
        username = ""
        if is_authenticated:
            username = request.user.username 
        context = {'navigation': final_list ,'is_authenticated' : is_authenticated , 'username' : username }
        print(context)
        return render(request, 'plagDetector/home.html', context)
    else:
        return render(request, 'plagDetector/home.html')


# function to upload multiples files
# files are stored in the ./media folder of the directory
def upload(request):
    if request.method == 'POST':
        for y, file in enumerate(request.FILES.getlist("document")):
            allowed_ext = ['txt', 'docx', 'doc']
            if file.name.split('.')[-1] not in allowed_ext:
                context = {'error': 'file extension not allowed, please upload a txt/doc/docx file!'}
                return render(request, 'plagDetector/home.html', context)

        for x, upload_file in enumerate(request.FILES.getlist("document")):
            print(upload_file.name)
            print(upload_file.size)
            fs = FileSystemStorage()
            fs.save(upload_file.name, upload_file, max_length=None)

    return render(request, 'plagDetector/home.html')



# need to implement
# only docx. or text files can be uploaded
