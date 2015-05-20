# coding=UTF-8
import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib import messages
from social.models import Gab
from core.models import User, Place, MailNotifications
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
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

        error = False

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")


        if not request.POST.get("last_name"):
            error = True
            messages.error(request, "Please give us your last name.")

        if not request.POST.get("first_name"):
            error = True
            messages.error(request, "Please give us your first name.")

        if not username:
            error = True
            messages.error(request, "Please give us your favorite username.")
        else:
            if User.objects.filter(username=username).exists():
                error = True
                messages.error(request, "This username is already used, please choose another one.")
            else:
                reg_username = re.compile("[a-z0-9_-]{3,16}")
                if not reg_username.match(username):
                    error = True
                    messages.error(request, "You must choose a valid username.")


        if not email:
            error = True
            messages.error(request, "Please give us your email.")
        else :
            if User.objects.filter(email=email).exists():
                error = True
                messages.error(request, "Someone already use this email. Please pick another one.")

        if not password:
            error = True
            messages.error(request, "You must choose a great password to protect your account.")

        if error:
            pre_form = {
                "email" : request.POST.get("email"),
                "username" : request.POST.get("username"),
                "first_name" : request.POST.get("first_name"),
                "last_name" : request.POST.get("last_name")
            }
            return render(request, "register.html", pre_form)

        else:
            new_place = Place()
            new_place.save()

            notifications = MailNotifications()
            notifications.save()

            user, created = User.objects.get_or_create(
                email=request.POST.get("email"),
                username=request.POST.get("username"),
                first_name=request.POST.get("first_name"),
                last_name=request.POST.get("last_name"),
                place=new_place,
                mail_notifications=notifications
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

            check_boxes = request.POST.getlist("notifications")

            request.user.mail_notifications.regab = False
            request.user.mail_notifications.like = False
            request.user.mail_notifications.private_message = False
            request.user.mail_notifications.citation = False

            if "regab" in check_boxes:
                request.user.mail_notifications.regab = True

            if "like" in check_boxes:
                request.user.mail_notifications.like = True

            if "private_message" in check_boxes:
                request.user.mail_notifications.private_message = True

            if "citation" in check_boxes:
                request.user.mail_notifications.citation = True


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
            request.user.mail_notifications.save()

        return HttpResponseRedirect("/update/")

    elif request.method == "GET":

        birthdate = ""
        if request.user.birthdate != None:
            birthdate =  request.user.birthdate.strftime('%d/%m/%Y')

        boole = bool(request.user.mail_notifications.regab)



        context = {
            "first_name":request.user.first_name,
            "last_name":request.user.last_name,
            "email":request.user.email,
            "birthdate":birthdate,
            "bool": boole,
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
        else:
            message = "Just a quick message to say goodbye :(\n"\
                "We hope you enjoyed to gab and spending time with us.\n\n"\
                "Thank you for your interest, Maybe will see you again later!\n"\
                "The gabbler team"

            send_mail("Goodbye dear friend",
                message,
                "gabbler.noreply@gmail.com",
                [request.user.email])

            request.user.delete()
            return HttpResponseRedirect("/")

    else:
        return render(request, "user/delete_profile.html")
