# coding=UTF-8

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
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
            username = request.POST.get("username")
            password = request.POST.get("password")
            return login(request, username, password)

        elif request.POST.get("redirection") == "new":

            request.session["data_register"] = {
                "username": request.POST.get("username_register"),
                "email": request.POST.get("email_register"),
                "password": request.POST.get("password_register")
            }
            return HttpResponseRedirect("/register")  # Redirection en cas d'autentification
    if request.user.is_authenticated():
        return render(request, "logged_index.html")
    return render(request, "guest_index.html")


def login(request, username, password):
    user = authenticate(username=username, password=password)
    if user:
        django_login(request, user)  # Fait la variable de session avec l'utilisateur dedans
        return HttpResponseRedirect("/")
    else:
        messages.error(request, "Username or password invalid")
        return HttpResponseRedirect("/connect")


def connect(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        return login(request, username, password)
    return render(request, "connect.html")


def register(request):
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user, created = User.objects.get_or_create(
            email=request.POST.get("email"),
            username=request.POST.get("username"),
            first_name=request.POST.get("first_name"),
            last_name=request.POST.get("last_name")
        )

        if created:
            user.set_password(password)
            user.save()

        user = authenticate(username=username, password=password)

        django_login(request, user)
        return HttpResponseRedirect("/")

    data = request.session.get("data_register")
    del request.session["data_register"]
    return render(request, "register.html", data)


def logout(request):
    django_logout(request)
    return HttpResponseRedirect("/")


def user_profile(request, username):
    user = User.objects.get(username=username)
    return render(request, "user/profile.html", {"req_user": user})