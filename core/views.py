from django.shortcuts import render


def home(request):
    return render(request, "index.html")

def connect(request) :
    return render(request, "connect.html")

def register(request) :
    return render(request, "register.html")


def test(request, toto):
    return render(request, "test.html", {"toto": toto})


def testpost(request):
    context = {}
    if request.method == "POST":
        context['name'] = request.POST.get("name")
    return render(request, "testpost.html", context)