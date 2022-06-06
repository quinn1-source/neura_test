from django.shortcuts import render, redirect
from django.conf import settings
# Create your views here.

DEBUG = False

def dashboard(request, *args, **kwargs):
    user = request.user

    # Redirect them if not authenticated
    if not user.is_authenticated:
        return redirect("login")

    context = {}
    context['debug'] = DEBUG
    context['debug_mode'] = settings.DEBUG
    return render(request, 'dashboard/dashboard.html', context)
