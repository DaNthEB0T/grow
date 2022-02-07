from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

def validation_required(function):
  @wraps(function)
  @login_required
  def wrap(request, *args, **kwargs):
      if not request.user.is_validated:
        return redirect("core:unvalidated")
      else:
        HttpResponseRedirect("/")
  return wrap