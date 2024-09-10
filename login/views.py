from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

def login(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("home:index", ))
    else:
        return render(request, 'login/index.html', {})

