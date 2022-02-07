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
        view_func(request, *args, **kwargs)
  return wrap