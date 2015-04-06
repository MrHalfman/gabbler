from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from models import Gab


@login_required
def post_gab(request):
    Gab.objects.create(
        user=request.user,
        text=request.POST.get("text")
    )
    return HttpResponseRedirect("/")
