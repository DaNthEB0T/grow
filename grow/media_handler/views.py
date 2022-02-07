import logging
from multiprocessing import context
from django.contrib import messages
import json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from core.decorators import validation_required
from .forms import ImageUploadForm, PostUploadForm
from .models import Post

# Create your views here.

@validation_required
def mh_view(request):
    context = {}
    if request.POST:
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.save(commit=False)
            img.author = request.user
            img.save()
    else:
        form = ImageUploadForm()
    context['form'] = form
    return render(request, "media_handler/index.html", context)

@validation_required
def post_handle_view(request):
    context = {}
    if request.POST:
        form = PostUploadForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            post = form.save()
            form.save_m2m()
            messages.success(request, "Post created successfuly")
            return redirect("media_handler:post", slug=post.slug)
    else:
        form = PostUploadForm(user=request.user)
    context['form'] = form
    return render(request, "media_handler/postu.html", context)

@validation_required
def post_view(request, slug):
    context = {}
    
    post = get_object_or_404(Post, slug=slug)
    user = request.user
    
    post.add_to_user_history(user)
    user.watchlist_posts.remove(post.id)
     
    saved = post in user.saved_posts.all()
    
    recommended = Post.get_recommended_posts(user, amount=8)
    context['recommended'] = {post: post in user.watchlist_posts.all() for post in recommended}

    context['post'] = post
    context['saved'] = saved
    return render(request, "media_handler/post.html", context)

@validation_required
def history_view(request):
    context = {}

    user = request.user

    history = Post.get_user_history(user).reverse()

    context['history'] = history
    
    return render(request, "media_handler/post_list/history.html", context)

@validation_required
@require_POST
def remove_from_history_view(request, slug):
    if request.POST:
        post = get_object_or_404(Post, slug=slug)
        
        user = request.user
        user.post_history.remove(post.id)
        
        return HttpResponse(content_type="application/json")

@validation_required
def saved_view(request):
    context = {}

    user = request.user

    saved_posts = Post.get_user_saved(user).reverse()

    context['saved_posts'] = saved_posts
    
    return render(request, "media_handler/post_list/saved.html", context)

@validation_required
@require_POST
def remove_from_saved_view(request, slug):
    if request.POST:
        post = get_object_or_404(Post, slug=slug)
        
        user = request.user
        user.saved_posts.remove(post.id)
        
        return HttpResponse(content_type="application/json")

@validation_required
def watchlist_view(request):
    context = {}

    user = request.user

    watchlist = Post.get_user_watchlist(user).reverse()

    context['watchlist'] = watchlist
    
    return render(request, "media_handler/post_list/watchlist.html", context)

@validation_required
@require_POST
def remove_from_watchlist_view(request, slug):
    if request.POST:
        post = get_object_or_404(Post, slug=slug)
        
        user = request.user
        user.watchlist_posts.remove(post.id)
        
        return HttpResponse(content_type="application/json")

@validation_required
@require_POST
def post_save_view(request, slug):
    if request.POST:
        post = get_object_or_404(Post, slug=slug)
        
        context = {}
        
        user = request.user
        saved = post.toggle_add_to_user_saved(user)
        
        context['saved'] = saved
        return HttpResponse(json.dumps(context), content_type="application/json")
        
@validation_required
@require_POST
def watch_later_view(request, slug):
    if request.POST:
        post = get_object_or_404(Post, slug=slug)
        
        context = {}
        
        user = request.user
        added = post.toggle_add_to_user_watchlist(user)
        
        context['added'] = added
        return HttpResponse(json.dumps(context), content_type="application/json")
