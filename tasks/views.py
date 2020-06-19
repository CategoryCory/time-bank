from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Task


class TaskRequestListView(ListView):
    model = Task
    queryset = Task.objects.filter(task_type='REQUEST', status='AVAILABLE')
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_type'] = 'requests'
        return context


class TaskOfferListView(ListView):
    model = Task
    queryset = Task.objects.filter(task_type='OFFER', status='AVAILABLE')
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_type'] = 'offers'
        return context


class TaskDetailView(DetailView):
    model = Task


class TaskRequestCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'expires_on', 'frequency', ]
    template_name_suffix = '_create_form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_type'] = 'request'
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.task_type = 'REQUEST'
        return super().form_valid(form)


class TaskOfferCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'expires_on', 'frequency', ]
    template_name_suffix = '_create_form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_type'] = 'offer'
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.task_type = 'OFFER'
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'expires_on', 'status', ]
    template_name_suffix = '_update_form'

    def test_func(self):
        obj = self.get_object()
        return obj.created_by == self.request.user


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name_suffix = '_confirm_delete'

    def test_func(self):
        obj = self.get_object()
        return obj.created_by == self.request.user

    def get_success_url(self):
        obj = self.get_object()
        if obj.task_type == 'REQUEST':
            return reverse_lazy('tasks:task_request_list')
        else:
            return reverse_lazy('tasks:task_offer_list')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.soft_delete()
        return HttpResponseRedirect(self.get_success_url())
