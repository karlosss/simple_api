from django.shortcuts import render


def serve_frontend(request):
    return render(request, "index.html", context={})
