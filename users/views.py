from django.views.generic.list import ListView
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class UserListView(ListView):
    model = CustomUser
    paginate_by = 25
