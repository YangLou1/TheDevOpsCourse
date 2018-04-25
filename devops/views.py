from django.shortcuts import render
from django.http import request

# Create your views here.

site_hdr = "Welcome to the DevOps course."  # type: str


def index(request: request)->object:
    return render(request, 'index.html', {'header': site_hdr})

def about(request: request)->object:
    return render(request, 'about.html', {'header': site_hdr})

