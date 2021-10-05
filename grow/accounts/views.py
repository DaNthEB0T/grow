from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import *


def registration_view(request):
    context = {}
    if request.POST:
        form = GrowUserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password1")

            user = authenticate(email=email, password=raw_password)
            login(request, user)

            return redirect("core-home")
    else:
        form = GrowUserRegistrationForm()

    context['registration_form'] = form
    return render(request, "accounts/register.html", context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect("core-home")

    context = {}

    if request.POST:
        form = GrowUserLoginForm(request.POST)
        if form.is_valid():

            email = form.cleaned_data.get("email").lower()
            raw_password = form.cleaned_data.get("password")

            user = authenticate(email=email, password=raw_password)
            try:
                login(request, user)
            except:
                pass

            return redirect("core-home")
    else:
        form = GrowUserLoginForm()

    context['login_form'] = form
    return render(request, "accounts/login.html", context)

def logout_view(request):
    logout(request)
    return redirect("core-home")