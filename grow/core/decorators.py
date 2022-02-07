from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def validation_required(function):
  @wraps(function)
  @login_required
  def wrap(request, *args, **kwargs):
      if not request.user.is_validated:
        return redirect("core:unvalidated")
  return wrap