from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.views import send_verification_email
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .decorators import validation_required
from media_handler.models import Post
from media_handler.recomai import search_posts

# Create your views here.

@validation_required
def dashboard_view(request):          
    context = {}
    
    search=False
    if "search" in request.POST:
        search=True
        search_phrase = request.POST.get("search")
        search_results = search_posts(search_phrase, amount=16)    
        context['recommended'] = {post: post in user.watchlist_posts.all() for post in search_results}
    else:
        recommended = Post.get_recommended_posts(user, amount=9)
        context['most_recommended'] = {post: post in user.watchlist_posts.all() for post in recommended[:1]}
        context['recommended'] = {post: post in user.watchlist_posts.all() for post in recommended[1:]}
        continue_watching = Post.get_user_history(user)
        context['continue'] = {post: post in user.watchlist_posts.all() for post in continue_watching[:1]}            
            
    context['search'] = search
    return render(request, "core/dashboard.html", context)

@login_required
def unvalidated_view(request):
    context = {}
    context['user'] = request.user
    
    if request.user.is_validated:
        return redirect("core:dashboard")
    
    if request.POST:
        if "resend_verification" in request.POST:
            send_verification_email(request, request.user)
            messages.info(request, _("Validation email has been sent"))
    
    return render(request, "core/unvalidated.html", context)

def error_404_view(request):
    return render(request, "core/errors/404.html")