# coding=UTF-8

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout as django_logout
from django.contrib import messages
from models import User


def home(request):
    if request.method == "POST":
        """
            POST.get() diffère de POST[] dans le sens où si le champ
            est vide, il remplacera le contenu par "None" au lieu de retourner
            une erreur.
        """
        if request.POST.get("redirection") == "connect":
            return HttpResponseRedirect("/connect")  # Redirection en cas d'autentification

            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)  # Fait la variable de session avec l'utilisateur dedans

            else:
                messages.error(request, "Username or password invalid")

        elif request.POST.get("redirection") == "new":

            request.session["data_register"] = {
                "username": request.POST.get("username_register"),
                "email": request.POST.get("email_register"),
                "password": request.POST.get("password_register")
            }
            return HttpResponseRedirect("/register")  # Redirection en cas d'autentification


    return render(request, "index.html")


def connect(request):
    return render(request, "connect.html")


def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        user, created = User.objects.get_or_create(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name
        )

        if created:
            user.set_password(password)
            user.save()

        user = authenticate(username=username, password=password)

        login(request, user)
        return HttpResponseRedirect("/")

    data = request.session.get("data_register")
    del request.session["data_register"]
    return render(request, "register.html", data)


def logout(request):
    django_logout(request)
    return HttpResponseRedirect("/")