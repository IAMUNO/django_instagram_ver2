from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse('<h1>Welcome to instagram</h1>')
