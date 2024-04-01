from django.shortcuts import render
from django.http import HttpResponse


def index(reguest):
    return render(reguest, 'main/home.html',{'title': "main"})

def about(reguest):
    data ={
        'title': "abooooout",
        'values' : ["some","lol",'ssdkk']
    }
    return render(reguest, 'main/about.html', data)