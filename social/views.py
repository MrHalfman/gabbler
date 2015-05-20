from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
import re
from social.models import Gab, AdditionalContent

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


@login_required
def post_gab(request):

    extra_content = AdditionalContent()
    extra_content.video = catch_video_link(request.POST.get("text"))
    extra_content.save()

    Gab.objects.create(
        user=request.user,
        text=request.POST.get("text"),
        extras=extra_content
    )
    return HttpResponseRedirect("/")

@login_required
def delete_gab(request, gab_pk):
    gab = Gab.objects.get(pk=gab_pk)
    gab.extras.delete()
    gab.delete()
    return HttpResponseRedirect("/")