from shutil import ExecError
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from .tokens import *
from .forms import *


def token_generated_email(request, user, email_subject, template_path, token_generator):
    current_site = get_current_site(request)
    user = user
    email_body = render_to_string(template_path,{
        'user': user,
        'domain': current_site.domain,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':token_generator.make_token(user),
    })

    email = EmailMessage(subject=email_subject, body=email_body, from_email=settings.EMAIL_HOST_USER, to=[user.email])
    email.send()

def send_verification_email(request, user):
    token_generated_email(request, user, email_subject="Verify your Grow account", template_path="accounts/emails/verification.html", token_generator=verification_token_generator)

def send_forgot_password_email(request, user):
    token_generated_email(request, user, email_subject="Grow Account Password Reset", template_path="accounts/emails/password_reset.html", token_generator=password_reset_token_generator)

# def registration_view(request):
#     if request.user.is_authenticated:
#         return redirect("core:dashboard")

#     context = {}
#     if request.POST:
#         form = GrowUserRegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()

#             email = form.cleaned_data.get("email")
#             raw_password = form.cleaned_data.get("password1")

#             user = authenticate(email=email, password=raw_password)
#             login_extended(request, user)

#             token_generated_email(request, request.user, email_subject="Verify your Grow account", template_path="accounts/emails/verification.html", token_generator=verification_token_generator)

#             return redirect("core:dashboard")
#     else:
#         form = GrowUserRegistrationForm()

#     context['registration_form'] = form
#     return render(request, "accounts/register.html", context)

def welcome_view(request):
    if request.user.is_authenticated:
        return redirect("core:dashboard")

    context = {}

    if request.POST:
        # Registration form
        registration_form = GrowUserRegistrationForm(request.POST)
        if registration_form.is_valid():
            registration_form.save()

            email = registration_form.cleaned_data.get("email")
            raw_password = registration_form.cleaned_data.get("password1")

            user = authenticate(email=email, password=raw_password)
            
            login_extended(request, user)
            
            try:
                send_verification_email(request, request.user)
            except Exception as e: 
                print(e)
            
            return redirect("core:dashboard")
        
        # Login form
        login_form = GrowUserLoginForm(request.POST)
        if login_form.is_valid():

            email = login_form.cleaned_data.get("email").lower()
            raw_password = login_form.cleaned_data.get("password")

            user = authenticate(email=email, password=raw_password)
            login_extended(request, user)

            return redirect("core:dashboard")
    else:
        login_form = GrowUserLoginForm()
        registration_form = GrowUserRegistrationForm()

    context['login_form'] = login_form
    context['registration_form'] = registration_form
    return render(request, "accounts/welcome.html", context)

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, _("Successfully logged out"))
    return redirect("core:dashboard")

def verification_view(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = GrowUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, GrowUser.DoesNotExist):
        user = None
    if user is not None and verification_token_generator.check_token(user, token):
        user.is_validated = True
        user.save()
        # DEBUG MESSAGE
        messages.success(request, _("Eyyy, validation successful"))
        # DEBUG MESSAGE
    else:
        messages.error(request, _("Something went wrong :("))

    return redirect("core:dashboard")

def forgot_password_view(request):
    context = {}

    if request.POST:
        forgot_password_form = GrowUserForgotPasswordForm(request.POST)
        if forgot_password_form.is_valid():
            user = GrowUser.objects.get(email=forgot_password_form.cleaned_data.get("email"))
            send_forgot_password_email(request, user)
            
        messages.info(request, _("Password reset link sent to email!"))                
    
    forgot_password_form = GrowUserForgotPasswordForm()
    context["forgot_password_form"] = forgot_password_form
    return render(request, "accounts/forgot_password.html", context)

def password_reset_view(request, uidb64, token):
    context = {}

    if request.POST:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = GrowUser.objects.get(pk=uid)
        form = GrowUserPasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Password successfully changed"))

            return redirect("accounts:login")
    else:
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = GrowUser.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, GrowUser.DoesNotExist):
            user = None
        if user is not None and password_reset_token_generator.check_token(user, token):
            form = GrowUserPasswordChangeForm(user)
            logout(request)
        else:
            # temp
            messages.error(request, _("Something went wrong :("))
            return redirect("core:dashboard")

    context["password_change_form"] = form

    return render(request, "accounts/password_reset.html", context)

def login_extended(request, user):
    if not user: 
        return
    login(request, user)
    messages.success(request, _(f"Successfully logged in as {user.username}"))

