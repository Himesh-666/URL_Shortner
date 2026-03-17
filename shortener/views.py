from django.shortcuts import render, redirect
from .models import URL
from .utils import generate_short_code


def home(request):

    if request.method == "POST":
        long_url = request.POST.get("url")

        code = generate_short_code()

        URL.objects.create(
            original_url=long_url,
            short_code=code
        )

        short_url = request.build_absolute_uri(code)

        return render(request, "shortener/home.html", {"short_url": short_url})

    return render(request, "shortener/home.html")


def redirect_url(request, code):

    url = URL.objects.get(short_code=code)

    return redirect(url.original_url)
# Create your views here.
