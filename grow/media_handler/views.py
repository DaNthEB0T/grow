from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import ImageUpload

# Create your views here.

@login_required
def index(request):
    context = {}
    if request.POST:
        form = ImageUpload(request.POST, request.FILES)
        if form.is_valid():
            img = form.save(commit=False)
            img.author = request.user
            img.save()
    else:
        form = ImageUpload()
    context['form'] = form
    return render(request, "media_handler/index.html", context)