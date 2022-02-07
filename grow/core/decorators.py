from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def validation_required(view_func):
  @wraps(view_func)
  @login_required
  def wrap(request, *args, **kwargs):
      if not request.user.is_validated:
        return redirect("core:unvalidated")
      else:
        return view_func(request, *args, **kwargs)
  return wrap

def unauthenticated_required(view_func):
  @wraps(view_func)
  def wrap(request, *args, **kwargs):
      if request.user.is_authenticated:
        return redirect("core:dashboard")
      else:
        return view_func(request, *args, **kwargs)
  return wrap