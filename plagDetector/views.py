from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
import nltk
from .forms import UploadFileForm
from django.core.files.storage import FileSystemStorage
from auth_app.models import User
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
# from pylab import rcParams
import matplotlib.pyplot as plt
#import seaborn as sns


#########################################################


def home(request):
    context = {'navigation': []}
    is_authenticated = request.user.is_authenticated
    notAuth = not is_authenticated
    username = ""
    if is_authenticated:
        username = request.user.username 
    context = {'is_authenticated' : is_authenticated , 'username' : username, "notAuth" : notAuth }
    return render(request, 'plagDetector/home.html', context)


# test function to compare two texts -Tanmay/Aadarsh/Aayush
def plag(text1, text2):
    str1 = ''.join(text1)
    str2 = ''.join(text2)

    similarity = get_similarity(str1, str2)
    print(similarity)


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
        context = {'navigation': final_list, 'is_authenticated': is_authenticated, 'username': username}
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


def cosine_func(X_list, Y_list):
    l1 = []
    l2 = []

    X_set = {w for w in X_list}
    Y_set = {w for w in Y_list}

    rvector = X_set.union(Y_set)
    for w in rvector:
        if w in X_set:
            l1.append(1)
        else:
            l1.append(0)
        if w in Y_set:
            l2.append(1)
        else:
            l2.append(0)
    c = 0

    for i in range(len(rvector)):
        c += l1[i] * l2[i]

    cosine = c / float((sum(l1) * sum(l2)) ** 0.5)
    return cosine * 100


def lcs(l1, l2):
    s1 = word_tokenize(l1)
    s2 = word_tokenize(l2)
    # storing the dp values
    dp = [[None] * (len(s1) + 1) for i in range(len(s2) + 1)]

    for i in range(len(s2) + 1):
        for j in range(len(s1) + 1):
            if i == 0 or j == 0:
                dp[i][j] = 0
            elif s2[i - 1] == s1[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[len(s2)][len(s1)]


def jc_func(tokens_o, tokens_p):
    l1 = []
    l2 = []
    s = 0

    for i in tokens_o:
        l1.append(i)

    for i in tokens_p:
        l2.append(i)
        if i in l1:
            s += 1

    # jaccord coefficient = (S(o)^S(p))/(S(o) U S(p))
    J = s / (len(set(l1).union(set(l2))))

    return J * 100


def max_lcs(orig, plag):
    sent_o = sent_tokenize(orig)
    sent_p = sent_tokenize(plag)
    word_o = word_tokenize(orig)
    word_p = word_tokenize(plag)

    # maximum length of LCS for a sentence in suspicious text
    max_lcs = 0
    sum_lcs = 0

    for i in sent_p:
        for j in sent_o:
            l = lcs(i, j)
            max_lcs = max(max_lcs, l)
        sum_lcs += max_lcs
        max_lcs = 0

    score = sum_lcs / len(set(word_o).union(set(word_p)))
    # print(score)
    return score * 100


def get_results(l1, l2):
    s1 = ""
    s2 = ""

    for i in l1:
        s1 = s1 + i + " ";
    for i in l2:
        s2 = s2 + i + " ";

    print("X: ", l1)
    print("\nY: ",l2)

    jaccard = jc_func(l1, l2)
    maxlcs = max_lcs(s1, s2)
    cosine = cosine_func(l1, l2)
    print("\nSimilarities detected by different algorithms:\n")
    print("\t Cosine: %.2f " % cosine, "%")
    print("\t Jaccard: %.2f" % jaccard, "%")
    print("\t Max largest common subsequence: %.2f" % maxlcs, "%")

    return (cosine, jaccard, maxlcs)


def get_only_results(l1, l2):
    s1 = ""
    s2 = ""

    for i in l1:
        s1 = s1 + i + " ";
    for i in l2:
        s2 = s2 + i + " ";

    jaccard = jc_func(l1, l2)
    maxlcs = max_lcs(s1, s2)
    cosine = cosine_func(l1, l2)

    return (cosine, jaccard, maxlcs)


def get_similarity(orig, plag):
    # tokanize
    tokens_o = word_tokenize(orig)
    tokens_p = word_tokenize(plag)

    # lowerCase
    tokens_o = [token.lower() for token in tokens_o]
    tokens_p = [token.lower() for token in tokens_p]

    stop_words = set(stopwords.words('english'))

    # remove stop words
    tokens_o = [w for w in tokens_o if not w in stop_words]
    tokens_p = [w for w in tokens_p if not w in stop_words]

    # remove punctuations
    punctuations = ['"', '.', '(', ')', ',', '?', ';', ':', "''", '``']

    tokens_o = [w for w in tokens_o if not w in punctuations]
    tokens_p = [w for w in tokens_p if not w in punctuations]

    # lemmatization
    lemmatizer = WordNetLemmatizer()

    tokens_o = [lemmatizer.lemmatize(w) for w in tokens_o]
    tokens_p = [lemmatizer.lemmatize(w) for w in tokens_p]

    # Calculate similarity and take the max value
    similarity = get_only_results(tokens_o, tokens_p)
    return similarity


def parse_file(file1, file2, directory):
    file1 = os.path.join(directory, file1)
    file2 = os.path.join(directory, file2)
    with open(file1, encoding='Latin-1') as file:
        data1 = file.read().replace('\n', '')
    with open(file2, encoding='Latin-1') as file:
        data2 = file.read().replace('\n', '')
    return (data1, data2)
