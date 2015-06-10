# coding=UTF-8
import datetime
import random
import string
import re

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib import messages
from core.models import User, MailNotifications
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string


def home(request):
    if request.user.is_authenticated():
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
                "email": request.POST.get("email_register")
            }
            return HttpResponseRedirect("/register")

    return render(request, "guest_index.html")


def login(request, username, password):
    user = authenticate(username=username, password=password)
    if user:
        django_login(request, user)
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
        password_confirm = request.POST.get("password-confirm")

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
        else:
            if password != password_confirm:
                error = True
                messages.error(request, "The confirmation of the password is not equal to the first field")
            else:
                reg_password = re.compile("(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}")
                if not reg_password.match(password):
                    error = True
                    messages.error(request, "The password must be contain at least 8 characters, one number "
                                            "and both lowercase and uppercase letters")

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

                mail_content = {
                    "mail_title": "Welcome " + request.POST.get("username") + "!",
                    "mail_body": "Just a short message to wish you a warm welcome! We hope you enjoy spending time with"
                                 " us :)"
                }
                html_content = render_to_string("mail_template.html", mail_content)
                string_content = "Welcome " + request.POST.get("username") + "!\n"\
                    "Just a short message to wish you a warm welcome! We hope you enjoy spending time with us :)\n\n"\
                    "The gabbler team"


                send_mail("Welcome!", string_content, "gabbler.noreply@gmail.com",
                [request.POST.get("email")], fail_silently=True, html_message=html_content)

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
    return render(request, "user/profile.html", {"req_user": user, "profile": True})


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
            mail_content = {
                "mail_title": "Just a quick message to say goodbye :(",
                "mail_body": "We hope you enjoyed to gab and spending time with us.\n\n"
                             "Thank you for your interest, Maybe will see you again later!"
            }
            html_content = render_to_string("mail_template.html", mail_content)
            string_content = "Just a quick message to say goodbye :(\n"\
                             "We hope you enjoyed to gab and spending time with us.\n\n"\
                             "Thank you for your interest, Maybe will see you again later!\n"\
                             "The gabbler team"

            send_mail("Goodbye dear friend", string_content, "gabbler.noreply@gmail.com", [request.user.email],
                      fail_silently=True, html_message=html_content)

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

            mail_content = {
                "mail_title": "Someone asked to change your password",
                "mail_body": "If you are the applicant, thank you to confirm the change with this code "
                             "***" + random_string + "***\n"
                             "If not, thank you to ignore this message."
            }
            html_content = render_to_string("mail_template.html", mail_content)
            string_content = "Someone asked to change your password. If you are the applicant, "\
                             "thank you to confirm the change with this code *** " + random_string + " ***\n"\
                             "If not, thank you to ignore this message.\n\n"\
                             "The gabbler team"

            send_mail("Recover your account", string_content, "gabbler.noreply@gmail.com", [request.POST.get("email")],
                      fail_silently=True, html_message=html_content)

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
                        mail_content = {
                            "mail_title": "Password changed",
                            "mail_body": "Your password has been changed successfully, welcome back " + user_list[0].username + "!"
                        }
                        html_content = render_to_string("mail_template.html", mail_content)
                        string_content = "Your password has been changed successfully, welcome back " + user_list[0].username + "!\n\n"\
                                         "The gabbler team"

                        send_mail("Password changed", string_content, "gabbler.noreply@gmail.com",
                                  [request.session.get("user_email")], fail_silently=True, html_message=html_content)

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
