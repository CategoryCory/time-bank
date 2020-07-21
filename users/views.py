from django.views.generic import DetailView, ListView, UpdateView, TemplateView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from tasks.models import Task

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


class UserDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'users/customuser_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_requests'] = Task.objects.filter(created_by=self.request.user, task_type=Task.REQUEST,
                                                       status=Task.AVAILABLE).order_by('expires_on')
        context['user_offers'] = Task.objects.filter(created_by=self.request.user, task_type=Task.OFFER,
                                                     status=Task.AVAILABLE).order_by('expires_on')
        return context
