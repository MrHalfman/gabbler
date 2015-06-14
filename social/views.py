from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
import re
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from core.models import User
from social.models import Gab, ModerationReport, Regab, GabOpinion, UserRelationships, Notifications
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

    gab.save()

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

    Notifications.objects.create(
        user=gab.user,
        text="%s regabbed your gab." % request.user.username,
        link="/gab/%d" % regab.pk
    )

    if not created:
        regab.delete()
    return HttpResponseRedirect("/user/%s" % gab.user.username)


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

    Notifications.objects.create(
        user=gab.user,
        text="%s liked your gab." % request.user.username,
        link="/gab/%d" % gab.pk
    )

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

    return HttpResponseRedirect("/user/%s" % usr.username)


@login_required
def mark_notifications_asread(request):
    request.user.unread_notifications.update(read=True)
    return JsonResponse({"success": True})


@login_required
def search(request, query):
    gabs = Gab.objects.filter(text__icontains=query)
    users = User.objects.filter(username__icontains=query)

    return render(request, "search.html", locals())


@login_required
def getGabs(request, page):
    gabs_per_page = 10
    min = int(page) * gabs_per_page
    max = min + gabs_per_page
    gabs = request.user.gabsfeed[min:max]

    return render(request, "skeletons/gabs_list.html", {"gabs": gabs})