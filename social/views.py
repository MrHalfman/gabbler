from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
import re
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from core.models import User
from social.models import Gab, AdditionalContent, ModerationReport, Regab, GabOpinion, UserRelationships
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


def catch_gifid(text):
    giphy_request = re.findall(r'G>(([a-zA-Z0-9]+(\+[a-zA-Z0-9]+)*))', text)
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

    if gif:
        gab.gifId = gif

    video = catch_video_link(text)
    if video:
        extra_content = AdditionalContent(
            video=video
        )
        extra_content.save()
        gab.extras = extra_content

    if gif or video:
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
