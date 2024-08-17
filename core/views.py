from django.shortcuts import render
from django.http import HttpResponse


def home_view(request):
    if request.method == "POST":
        user_input = request.POST.get("user_input")

        return HttpResponse(f"Received text: {user_input}")

    return render(request, "core/home.html")
