from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.conf import settings
from .tokens import *
from .forms import *

@login_required
def token_generated_email(request, email_subject, template_path):
    current_site = get_current_site(request)
    user = request.user
    email_body = render_to_string(template_path,{
        'user': user,
        'domain': current_site.domain,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':token_generator.make_token(user),
    })

    email = EmailMessage(subject=email_subject, body=email_body, from_email=settings.EMAIL_HOST_USER, to=[user.email])
    email.send()


def registration_view(request):
    if request.user.is_authenticated:
        return redirect("core:home")

    context = {}
    if request.POST:
        form = GrowUserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password1")

            user = authenticate(email=email, password=raw_password)
            login(request, user)

            token_generated_email(request, email_subject="Verify your Grow account", template_path="accounts/verification.html")

            return redirect("core:home")
    else:
        form = GrowUserRegistrationForm()

    context['registration_form'] = form
    return render(request, "accounts/register.html", context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect("core:home")

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

            return redirect("core:home")
    else:
        form = GrowUserLoginForm()

    context['login_form'] = form
    return render(request, "accounts/login.html", context)

def logout_view(request):
    logout(request)
    return redirect("core:home")

def verification_view(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = GrowUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, GrowUser.DoesNotExist):
        user = None
    if user is not None and token_generator.check_token(user, token):
        user.is_validated = True
        user.save()

    return redirect("core:home")