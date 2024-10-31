from django.shortcuts import render

def netics_home (request) :
    return render (request, "mainPage/index.html", {})