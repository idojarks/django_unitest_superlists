from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

def login_custom(request):
    user = authenticate(request.POST['email'])
    if user:
        login(request, user)
    return HttpResponse('OK')