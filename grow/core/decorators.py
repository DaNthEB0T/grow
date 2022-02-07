from functools import wraps
from django.shortcuts import redirect

def validation_required(function):
  @wraps(function)
  def wrap(request, *args, **kwargs):
      if not request.user.is_validated:
        return redirect("core:unvalidated")
  return wrap