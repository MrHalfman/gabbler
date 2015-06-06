# coding=UTF-8
import datetime
import random
import string
import re
import json
import urllib2

from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib import messages
from social.models import Gab
from core.models import User, Place, MailNotifications
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail


def get_gif(gab):
    giphy_request = re.findall(r'G>(([a-zA-Z0-9]+(\+[a-zA-Z0-9]+)*))', gab.text)
    """if giphy_request:
        get_parameters = "+".join(str(id[0]) for id in giphy_request)
        url = "http://api.giphy.com/v1/gifs/search?q=" + get_parameters + "&limit=1&api_key=dc6zaTOxFJmzC"
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        if response:
            decoded_json = json.loads(response.read())
            if decoded_json["data"]:
                gab.giphy = decoded_json["data"][0]["embed_url"]"""

# ######################################################################################################################
# ######################################################################################################################


def home(request):
    if request.user.is_authenticated():
        # Add a new field in the gab for the YouTube link (display it in an iframe later)
        for gab in request.user.gabs.all():
            get_gif(gab)

        context = {
            "req_user": request.user
        }
        return render(request, "user/profile.html", context)

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

    return render(request, "guest_index.html")


def login(request, username, password):
    user = authenticate(username=username, password=password)
    if user:
        django_login(request, user)  # Fait la variable de session avec l'utilisateur dedans
        if request.GET.get("next"):
            return HttpResponseRedirect(request.GET.get("next"))
        else:
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
        else:
            if User.objects.filter(email=email).exists():
                error = True
                messages.error(request, "Someone already use this email. Please pick another one.")

        if not password:
            error = True
            messages.error(request, "You must choose a great password to protect your account.")

        if error:
            pre_form = {
                "email": request.POST.get("email"),
                "username": request.POST.get("username"),
                "first_name": request.POST.get("first_name"),
                "last_name": request.POST.get("last_name")
            }
            return render(request, "register.html", pre_form)

        else:
            notifications = MailNotifications()
            notifications.save()

            user, created = User.objects.get_or_create(
                email=request.POST.get("email"),
                username=request.POST.get("username"),
                first_name=request.POST.get("first_name"),
                last_name=request.POST.get("last_name"),
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


@login_required
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

            if request.POST.get("city") or request.POST.get("country"):
                request.user.place.city = request.POST.get("city")
                request.user.place.country = request.POST.get("country")
            elif request.user.place:
                request.user.place.delete()

            check_boxes = request.POST.getlist("notifications")

            request.user.mail_notifications.regab = "regab" in check_boxes
            request.user.mail_notifications.like = "like" in check_boxes
            request.user.mail_notifications.private_message = "private_message" in check_boxes
            request.user.mail_notifications.citation = "citation" in check_boxes

            if request.POST.get("birthdate") != "":
                try:
                    request.user.birthdate = datetime.datetime.strptime(request.POST.get("birthdate"), "%d/%m/%Y")
                except ValueError:
                    messages.error(request, "You must choose a date from the date picker.")
            else:
                request.user.birthdate = None

            if request.POST.get("new-password"):
                request.user.set_password(request.POST.get("new-password"))

            if request.FILES.get("avatar"):
                request.user.avatar = request.FILES["avatar"]

            if request.FILES.get("banner"):
                request.user.banner = request.FILES["banner"]

            request.user.save()
            request.user.place.save()
            request.user.mail_notifications.save()

        return HttpResponseRedirect("/update/")

    elif request.method == "GET":
        birthdate = ""
        if request.user.birthdate is not None:
            birthdate = request.user.birthdate.strftime('%d/%m/%Y')

        boole = bool(request.user.mail_notifications.regab)

        context = {
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": request.user.email,
            "birthdate": birthdate,
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

            send_mail(
                "Goodbye dear friend",
                message,
                "gabbler.noreply@gmail.com",
                [request.user.email])

            request.user.delete()
            return HttpResponseRedirect("/")

    else:
        return render(request, "user/delete_profile.html")


def lost_password_step_1(request):
    if request.method == "POST":
        error = False

        if request.POST.get("email") == "":
            error = True
            messages.error(request, "You must give us a valid email.")
        elif not User.objects.filter(email=request.POST.get("email")):
            error = True
            messages.error(request, "No account is attached to this email.")

        if not error:
            random_string = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            request.session["check_password"] = random_string
            request.session["user_email"] = request.POST.get("email")

            message = "Someone asked to change your password. If you are the applicant, "\
                      "thank you to confirm the change with this code *** " + random_string + " ***\n\n"\
                      "If not, thank you to ignore this message.\n"\
                      "The gabbler team"
            send_mail("Update your password", message, "gabbler.noreply@gmail.com", [request.POST.get("email")])
            return HttpResponseRedirect("/lost_password-step-2/")

    return render(request, "user/lost_password_step_1.html")


def lost_password_step_2(request):
    if request.session.get("check_password"):

        if request.method == "POST":
            error = False
            context = {
                "check_code": ""
            }

            if request.POST.get("code") == "":
                error = True
                messages.error(request, "You must enter the code that was sent to you by email.")
            elif request.POST.get("code") != request.session.get("check_password"):
                error = True
                messages.error(request, "Wrong code, please check your email.")
            else:
                context["check_code"] = request.POST.get("code")

            if request.POST.get("new-password") == "" or request.POST.get("new-password-confirm") == "":
                error = True
                messages.error(request, "You must fill the two password fields.")
            elif request.POST.get("new-password") != request.POST.get("new-password-confirm"):
                error = True
                messages.error(request, "The two passwords aren't equals.")

            if not error:
                query = User.objects.filter(email=request.session.get("user_email"))
                user_list = list(query[:1])
                if user_list:
                    user_list[0].set_password(request.POST.get("new-password"))
                    user_list[0].save()
                    context["confirm_message"] = True

                    if request.session.get("user_email"):
                        message = "Your password has been changed successfully, welcome back " + user_list[0].username + "!\n"\
                                  "The gabbler team"
                        send_mail("Update your password", message, "gabbler.noreply@gmail.com", [request.session.get("user_email")])

                    del request.session["user_email"]
                    del request.session["check_password"]

                    return render(request, "user/lost_password_step_2.html", context)
                else:
                    messages.error(request,
                                   "A problem occurred when changing the password. Sorry for the inconvenience.")
            else:
                return render(request, "user/lost_password_step_2.html", context)

    else:
        return HttpResponseRedirect("/lost_password-step-1/")

    return render(request, "user/lost_password_step_2.html")
