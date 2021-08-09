from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.urls import reverse_lazy

CustomUser = get_user_model()


def login_success(request):
    if request.user.is_authenticated:
        if request.user.last_name is None or request.user.last_name == '':
            return redirect(reverse_lazy('dashboard:user_update', kwargs={'username': request.user.username}))
        else:
            return redirect(reverse_lazy('pages:home'))
    else:
        return redirect(reverse_lazy('pages:home'))