from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index_view(request):          
    context = {}
    context['user'] = request.user
    return render(request, "core/index.html", context)

def error_404_view(request):
    return render(request, "core/errors/404.html")