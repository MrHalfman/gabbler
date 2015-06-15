from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
import re
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from core.models import User
from social.models import Gab, ModerationReport, Regab, GabOpinion, UserRelationships, Notifications
from django.template.loader import render_to_string
from django.core.mail import send_mail as django_send_mail
import urllib2
import json


def catch_video_link(gab):
    youtube_link = re.search(r'(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/[^ ]+', gab)
    if youtube_link:
        embed_link = re.search(r'(https?\:\/\/)?www\.youtube\.com\/embed\/[^ ]+', youtube_link.group())
        if embed_link:
            return youtube_link.group()
        else:
            id_video = youtube_link.group().split("=")[1]
            id_video = re.search(r'[^ =&]+', id_video)
            if id_video:
                return "http://www.youtube.com/embed/" + id_video.group()
    return False


def catch_photo_link(gab):
    photo_link = re.search(r'(https?\:\/\/)?[$\-./+!*(),\w]+/[\w-]+\.(png|jpg|gif)', gab)
    if photo_link:
        return photo_link.group()
    return False


def catch_gifid(text):
    giphy_request = re.findall(r'g/(([a-zA-Z0-9]+(\+[a-zA-Z0-9]+)*))', text)
    if giphy_request:
        get_parameters = "+".join(str(id[0]) for id in giphy_request)
        url = "http://api.giphy.com/v1/gifs/search?q=" + get_parameters + "&limit=1&api_key=l41lICEpoxH594Kly"
        req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
        response = urllib2.urlopen(req)
        if response:
            decoded_json = json.loads(response.read())
            if decoded_json["data"]:
                return decoded_json["data"][0]["id"]
    return False


def send_mail(user, title, html_body, text, type):
    if not getattr(user.mail_notifications, type):
        return False

    mail_content = {
        "mail_title": title,
        "mail_body": html_body
    }
    html_content = render_to_string("mail_template.html", mail_content)
    string_content = text

    django_send_mail(
        "Welcome!",
        string_content,
        "gabbler.noreply@gmail.com",
        [user.email],
        fail_silently=True,
        html_message=html_content
    )


@login_required
def post_gab(request):
    text = request.POST.get("text")
    gab = Gab(
        user=request.user,
        text=text
    )

    gif = catch_gifid(text)
    video = catch_video_link(text)
    picture = catch_photo_link(text)

    if gif:
        gab.gif_id = gif

    if video:
        gab.video = video

    if picture:
        gab.picture = picture

    regex = re.compile('(@\w+)')
    userlist = regex.findall(text)

    gab.save()

    notifications_bulk = []
    for uname in userlist:
        try:
            user = User.objects.get(username=uname[1:])
            text = "%s mentioned your name in a gab." % request.user.username
            notifications_bulk.append(Notifications(
                user=user,
                text=text,
                link="/gab/%d" % gab.pk
            ))
            send_mail(user, "You have been mentioned on Gabbler.", text, text, "citation")
        except User.DoesNotExist:
            pass

    Notifications.objects.bulk_create(notifications_bulk)

    return HttpResponseRedirect("/")


@login_required
def delete_gab(request, gab_pk):
    Gab.objects.filter(pk=gab_pk).delete()
    return HttpResponseRedirect("/")


@csrf_exempt
@login_required
def report_gab(request, gab_pk):
    gab = Gab.objects.get(pk=gab_pk)
    ModerationReport.objects.create(
        by=request.user,
        gab=gab,
        reason=request.GET.get("reason")
    )
    return JsonResponse({"success": True})


@staff_member_required
@login_required
def moderation_reports(request):
    reports = ModerationReport.objects.filter(processed=False)
    return render(request, "admin/moderation_reports.html", locals())


@staff_member_required
@login_required
def moderation_reports_processed(request, report_pk):
    report = ModerationReport.objects.get(pk=report_pk)
    report.processed = True
    report.save()
    return HttpResponseRedirect("/admin/reports/")


@login_required
def regab(request, gab_pk):
    gab = Gab.objects.get(pk=gab_pk)
    regab, created = Regab.objects.get_or_create(
        gab=gab,
        user=request.user
    )
    regabbed = created

    if not created:
        regab.delete()
    else:
        text = "%s regabbed your gab." % request.user.username
        Notifications.objects.create(
            user=gab.user,
            text=text,
            link="/gab/%d" % regab.pk
        )
        send_mail(gab.user, "One of your gabs has been regabbed.", text, text, "regab")

    return JsonResponse({
        "success": True,
        "regabbed": regabbed,
        "regabs": gab.regabs.count()
    })


@login_required
def like(request, gab_pk):
    gab = Gab.objects.get(pk=gab_pk)
    opinion, created = GabOpinion.objects.get_or_create(
        user=request.user,
        gab=gab
    )
    response = {
        "success": True
    }

    if not created and opinion.like is True:
        opinion.delete()
    else:
        opinion.like = True
        opinion.save()
        response['liking'] = True
        text = "%s liked your gab." % request.user.username
        if gab.user != request.user:
            Notifications.objects.create(
                user=gab.user,
                text=text,
                link="/gab/%d" % gab.pk
            )
            send_mail(gab.user, "One of your gabs has been liked.", text, text, "like")

    response['likes'] = gab.likes.count()
    response['dislikes'] = gab.dislikes.count()

    return JsonResponse(response)


@login_required
def dislike(request, gab_pk):
    gab = Gab.objects.get(pk=gab_pk)
    opinion, created = GabOpinion.objects.get_or_create(
        user=request.user,
        gab=gab
    )
    response = {
        "success": True
    }

    if not created and opinion.like is False:
        opinion.delete()
    else:
        opinion.like = False
        opinion.save()
        response['disliking'] = True

    response['dislikes'] = gab.dislikes.count()
    response['likes'] = gab.likes.count()

    return JsonResponse(response)


@login_required
def follow(request, user_pk):
    usr = User.objects.get(pk=user_pk)
    relationship, created = UserRelationships.objects.get_or_create(
        user=request.user,
        following=usr
    )

    if not created:
        relationship.delete()
    else:
        Notifications.objects.create(
            user=usr,
            text="%s followed you." % request.user.username,
            link="/user/%s" % request.user.username
        )

    return HttpResponseRedirect("/user/%s" % usr.username)


@login_required
def mark_notifications_asread(request):
    request.user.unread_notifications.update(read=True)
    return JsonResponse({"success": True})


@login_required
def search(request, query):
    words = query.split(" ")
    gabs = list()
    users = list()

    for word in words:
        gabs += list(Gab.objects.filter(text__icontains=word))
        users += list(User.objects.filter(username__icontains=word))

    return render(request, "search.html", locals())


@login_required
def getGabs(request, page=0):
    gabs_per_page = 10
    min = int(page) * gabs_per_page
    max = min + gabs_per_page
    gabs = request.user.gabsfeed[min:max]

    return render(request, "skeletons/gabs_list.html", {"gabs": gabs})


@login_required
def getGab(request, pk):
    return render(request, "social/gab.html", {"gab": Gab.objects.get(pk=pk)})
