from django.views.generic import DetailView, ListView, UpdateView, TemplateView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

CustomUser = get_user_model()


class UserListView(ListView):
    model = CustomUser
    paginate_by = 25


class UserDetailView(DetailView):
    model = CustomUser
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomUser
    fields = ['first_name', 'last_name', 'username', 'date_of_birth', 'biography', 'profile_pic', ]
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name_suffix = '_update_form'

    def test_func(self):
        obj = self.get_object()
        return obj == self.request.user


class UserDashboardView(TemplateView):
    template_name = 'users/customuser_dashboard.html'
