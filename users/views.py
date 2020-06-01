from django.views.generic import DetailView, ListView
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class UserListView(ListView):
    model = CustomUser
    paginate_by = 25


class UserDetailView(DetailView):
    model = CustomUser
    slug_field = 'username'
    slug_url_kwarg = 'username'
