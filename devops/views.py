from django.shortcuts import render

# Create your views here.

site_hdr = "Welcome to the DevOps course."


def index(request):
    return render(request, 'index.html', {'header': site_hdr})

def about(request):
    return render(request, 'about.html', {'header': site_hdr})

