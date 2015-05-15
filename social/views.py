from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from social.models import Gab


@login_required
def post_gab(request):
    Gab.objects.create(
        user=request.user,
        text=request.POST.get("text")
    )
    return HttpResponseRedirect("/")

def delete_gab(request, gab_pk):
    gab = Gab.objects.get(pk=gab_pk)
    gab.delete()
    return HttpResponseRedirect("/")