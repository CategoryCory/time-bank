from django.views.generic import DetailView, ListView, UpdateView, TemplateView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from tasks.models import Task, Response

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
        user_tasks = Task.objects.filter(created_by=self.request.user, status=Task.AVAILABLE)

        user_requests = [user_req for user_req in user_tasks if user_req.task_type == Task.REQUEST]
        user_offers = [user_offer for user_offer in user_tasks if user_offer.task_type == Task.OFFER]

        context['user_requests'] = sorted(user_requests, key=lambda x: x.expires_on)
        context['user_offers'] = sorted(user_offers, key=lambda x: x.expires_on)

        return context


class UserMessageListView(LoginRequiredMixin, TemplateView):
    template_name = 'users/customuser_message_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_messages = Response.objects.filter(recipient=self.request.user)
        context['user_messages'] = user_messages
        return context


class UserMessageDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Response
    template_name = 'users/customuser_message_detail.html'

    def test_func(self):
        obj = self.get_object()
        return obj.recipient == self.request.user
