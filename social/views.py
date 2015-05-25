from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
import re
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from social.models import Gab, AdditionalContent, ModerationReport


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


@login_required
def post_gab(request):
    gab = Gab.objects.create(
        user=request.user,
        text=request.POST.get("text")
    )

    video = catch_video_link(request.POST.get("text"))
    if video:
        extra_content = AdditionalContent(
            video=video
        )
        extra_content.save()
        gab.extras = extra_content
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