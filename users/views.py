from django.views.generic import DetailView, ListView, UpdateView
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class UserListView(ListView):
    model = CustomUser
    paginate_by = 25


class UserDetailView(DetailView):
    model = CustomUser
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserUpdateView(UpdateView):
    model = CustomUser
    fields = ['first_name', 'last_name', 'date_of_birth', 'biography', ]
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name_suffix = '_update_form'
