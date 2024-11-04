from django.shortcuts import render
from .context import context

def netics_home (request) :

    return render (request, "mainPage/index.html", context)

def myNetwork (request): 
    return render (request, "myNetwork/index.html", {})
