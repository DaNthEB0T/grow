from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import ImageUploadForm, PostUploadForm

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
    else:
        form = PostUploadForm(user=request.user)
    context['form'] = form
    return render(request, "media_handler/postu.html", context)