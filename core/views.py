# coding=UTF-8

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib import messages
from social.models import Gab
from core.models import User
import re

def encode_string_with_links(unencoded_string):
    return URL_REGEX.sub(r'<a href="\1">\1</a>', unencoded_string)


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
        gabs = Gab.objects.filter(user=request.user)

        # Add a new field in the gab for the YouTube link (display it in an iframe later)
        for gab in gabs:
            youtubeLink = re.search(r'(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/[^ ]+', gab.text)
            if youtubeLink:
                embedLink = re.search(r'(https?\:\/\/)?www\.youtube\.com\/embed\/[^ ]+', youtubeLink.group())
                if embedLink:
                    gab.youtubeLink = youtubeLink.group()
                else:
                    idVideo = youtubeLink.group().split("=")[1]
                    idVideo = re.search(r'[^ =&]+', idVideo)
                    if idVideo:
                        gab.youtubeLink = "http://www.youtube.com/embed/" + idVideo.group()

        context = {
            "gabs": gabs
        }
        return render(request, "logged_index.html", context)

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