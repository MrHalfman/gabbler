# coding=UTF-8
import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib import messages
from social.models import Gab
from core.models import User, Place
from django.contrib.auth.decorators import login_required
import re
import json
import urllib2


"""
def links_to_tags(text):
    url_regex = re.compile(r'((https?:\/\/)?(www)?([\da-z\.-]+)\.([a-zA-Z-\.]{2,6})\/?[\/\w\.\?=&-]*\/?)')
    return url_regex.sub(r'<a href="\1">\1</a>', text)
"""

def get_gif(gab):
    giphy_request = re.findall(r'G>(([a-zA-Z0-9]+(\+[a-zA-Z0-9]+)*))', gab.text)
    if giphy_request:
        get_parameters = "+".join(str(id[0]) for id in giphy_request)
        url = "http://api.giphy.com/v1/gifs/search?q=" + get_parameters + "&limit=1&api_key=dc6zaTOxFJmzC"
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        if response:
            decoded_json = json.loads(response.read())
            if decoded_json["data"]:
                gab.giphy = decoded_json["data"][0]["embed_url"]

def get_video(gab):
    youtube_link = re.search(r'(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/[^ ]+', gab.text)
    if youtube_link:
        embed_link = re.search(r'(https?\:\/\/)?www\.youtube\.com\/embed\/[^ ]+', youtube_link.group())
        if embed_link:
            gab.youtube_link = youtube_link.group()
        else:
            id_video = youtube_link.group().split("=")[1]
            id_video = re.search(r'[^ =&]+', id_video)
            if id_video:
                gab.youtube_link = "http://www.youtube.com/embed/" + id_video.group()


# ######################################################################################################################
# ######################################################################################################################

def home(request):
    if request.method == "POST":
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
        gabs = Gab.objects.filter(user=request.user).order_by('-date')

        # Add a new field in the gab for the YouTube link (display it in an iframe later)
        for gab in gabs:
            get_gif(gab)
            get_video(gab)

        place_elements = ""
        if request.user.place:
            place_elements = request.user.place.city, request.user.place.country
            place_elements = filter(None, place_elements)

        context = {
            "place": ", ".join(place_elements),
            "birthdate": request.user.birthdate,
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
        new_place = Place()
        new_place.save()

        user, created = User.objects.get_or_create(
            email=request.POST.get("email"),
            username=request.POST.get("username"),
            first_name=request.POST.get("first_name"),
            last_name=request.POST.get("last_name"),
            place=new_place
        )

        if created:
            user.set_password(password)
            user.save()

        user = authenticate(username=username, password=password)

        django_login(request, user)
        return HttpResponseRedirect("/")

    data = request.session.get("data_register")
    if data:
        del request.session["data_register"]
    return render(request, "register.html", data)


def logout(request):
    django_logout(request)
    return HttpResponseRedirect("/")


def user_profile(request, username):
    user = User.objects.get(username=username)
    return render(request, "user/profile.html", {"req_user": user})


@login_required
def update(request):
    if request.method == "POST":
        error = False

        if not request.POST.get("first_name"):
            error = True
            messages.error(request, "Please give us your first name.")

        if not request.POST.get("last_name"):
            error = True
            messages.error(request, "Please give us your last name.")

        if not request.POST.get("email"):
            error = True
            messages.error(request, "Please give us your email.")

        if not request.user.check_password(request.POST.get("old-password")):
            error = True
            messages.error(request, "Please type your password before validate your modifications.")

        if request.POST.get("new-password") != request.POST.get("new-password-confirm"):
            error = True
            messages.error(request, "Password and confirmation passwords aren't the same.")

        if not error:
            request.user.first_name = request.POST.get("first_name")
            request.user.last_name = request.POST.get("last_name")
            request.user.email = request.POST.get("email")
            request.user.place.city = request.POST.get("city")
            request.user.place.country = request.POST.get("country")

            if request.POST.get("birthdate") != "":
                try :
                    request.user.birthdate = datetime.datetime.strptime(request.POST.get("birthdate"), "%d/%m/%Y")
                except :
                    messages.error(request, "You must choose a date from the date picker.")
            else:
                request.user.birthdate = None

            if request.POST.get("new-password"):
                request.user.set_password(request.POST.get("new-password"))

            request.user.save()
            request.user.place.save()

        return HttpResponseRedirect("/update/")

    elif request.method == "GET":

        birthdate = ""
        if request.user.birthdate != None:
            birthdate =  request.user.birthdate.strftime('%d/%m/%Y')

        context = {
            "first_name":request.user.first_name,
            "last_name":request.user.last_name,
            "email":request.user.email,
            "city":request.user.place.city,
            "country":request.user.place.country,
            "birthdate":birthdate,
            "update_flag": True
        }

        return render(request, "user/update_profile.html", context)

@login_required
def delete_user(request):
    if request.method == "POST":
        if not request.user.check_password(request.POST.get("password")):
            error = True
            messages.error(request, "Please type your correct password before validate the deletion.")

            if error:
                return HttpResponseRedirect("user/delete_profile.html")
        else :
            request.user.delete()
            return HttpResponseRedirect("/")

    else:
        return render(request, "user/delete_profile.html")
