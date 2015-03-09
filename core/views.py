# coding=UTF-8

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib import messages


def home(request):
    if request.method == "POST":
        """
            POST.get() diffère de POST[] dans le sens où si le champ
            est vide, il remplacera le contenu par "None" au lieu de retourner
            une erreur.
        """
        if request.POST.get("redirection") == "connect" :
            return HttpResponseRedirect("/connect") # Redirection en cas d'autentification

            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(username = username, password = password)

            if user:
                login(request, user) # Fait la variable de session avec l'utilisateur dedans

            else:
                messages.error(request, "Username or password invalid")

        else:
            return HttpResponseRedirect("/register") # Redirection en cas d'autentification

    return render(request, "index.html")

def connect(request) :
    return render(request, "connect.html")


def register(request) :
    return render(request, "register.html")


def test(request, toto):
    return render(request, "test.html", {"toto": toto})


def testpost(request):
    context = {}
    if request.method == "POST":
        context['name'] = request.POST.get("name")
    return render(request, "testpost.html", context)