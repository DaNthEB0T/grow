from django.contrib import messages
import json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import ImageUploadForm, PostUploadForm
from .models import Post

# Create your views here.

@login_required
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

@login_required
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

@login_required
def post_view(request, slug):
    context = {}
    
    post = get_object_or_404(Post, slug=slug)
    user = request.user
    
    post.add_to_user_history(user)
     
    saved = post in user.saved_posts.all()

    context['post'] = post
    context['saved'] = saved
    return render(request, "media_handler/post.html", context)

@login_required
@require_POST
def post_save_view(request, slug):
    if request.POST:
        post = get_object_or_404(Post, slug=slug)
        
        context = {}
        
        user = request.user
        saved = post.toggle_add_to_user_saved(user)
        
        context['saved'] = saved
        return HttpResponse(json.dumps(context), content_type="application/json")
        
@login_required
@require_POST
def watch_later_view(request, slug):
    if request.POST:
        post = get_object_or_404(Post, slug=slug)
        
        context = {}
        
        user = request.user
        added = post.toggle_add_to_user_watchlist(user)
        
        context['added'] = added
        return HttpResponse(json.dumps(context), content_type="application/json")
