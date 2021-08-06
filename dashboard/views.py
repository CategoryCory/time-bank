import datetime
from django.db import transaction
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from reviews.models import UserReview
from tasks.models import Task, TaskResponse
from tasks.forms import TaskForm, TaskAvailabilityFormSet
from dashboard.forms import UserUpdateForm

CustomUser = get_user_model()


class UserDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_jobs = Task.objects.filter(
            created_by=self.request.user,
            status=Task.AVAILABLE
        ).order_by('expires_on')
        context['user_jobs'] = user_jobs
        return context


class PendingResponsesView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard_pending_responses.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pending_responses = TaskResponse.objects.filter(
            recipient=self.request.user,
            status=TaskResponse.PENDING
        ).order_by('created_by')
        context['pending_responses'] = pending_responses
        return context


class AcceptedResponsesView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard_accepted_responses.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        accepted_responses = TaskResponse.objects.filter(
            recipient=self.request.user,
            status=TaskResponse.ACCEPTED
        )
        context['accepted_responses'] = accepted_responses
        return context


class CompletedResponsesView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard_completed_responses.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        completed_responses = TaskResponse.objects.filter(
            recipient=self.request.user,
            status=TaskResponse.COMPLETED
        )
        context['completed_responses'] = completed_responses
        return context


class SentResponsesView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard_sent_responses.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sent_responses = TaskResponse.objects.filter(
            created_by=self.request.user
        )
        context['sent_responses'] = sent_responses
        return context


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomUser
    form_class = UserUpdateForm
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'dashboard/dashboard_update_profile.html'

    def test_func(self):
        obj = self.get_object()
        return obj == self.request.user


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'dashboard/dashboard_task_create_form.html'
    # template_name_suffix = '_create_form'
    success_url = reverse_lazy('dashboard:dashboard_home')

    def get_context_data(self, **kwargs):
        data = super(TaskCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['availabilities'] = TaskAvailabilityFormSet(self.request.POST)
        else:
            data['availabilities'] = TaskAvailabilityFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        availabilities = context['availabilities']
        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()
            if availabilities.is_valid():
                availabilities.instance = self.object
                availabilities.save()
        return super(TaskCreateView, self).form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'expires_on', 'status', ]
    template_name = 'dashboard/dashboard_task_update_form.html'
    success_url = reverse_lazy('dashboard:dashboard_home')
    # template_name_suffix = '_update_form'

    def test_func(self):
        obj = self.get_object()
        return obj.created_by == self.request.user


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'dashboard/dashboard_task_confirm_delete.html'
    # template_name_suffix = '_confirm_delete'

    def test_func(self):
        obj = self.get_object()
        return obj.created_by == self.request.user

    def get_success_url(self):
        # obj = self.get_object()
        return reverse_lazy('dashboard:dashboard_home')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.soft_delete()
        return HttpResponseRedirect(self.get_success_url())


@login_required
def record_time(request, response_id):
    rsp = get_object_or_404(TaskResponse, pk=response_id)

    if request.method == 'GET':
        context = {
            'response_id': response_id,
            'job_title': rsp.task.title,
            'job_user': f'{rsp.created_by.first_name} {rsp.created_by.last_name}',
            'max_hours': rsp.recipient.sullivan_coins_balance
        }
        return render(request, 'dashboard/dashboard_task_record_time.html', context)
    elif request.method == 'POST':
        number_of_hours = float(request.POST.get('numberOfHours'))
        job_performed_by = rsp.created_by
        current_user = request.user
        job_performed_by.sullivan_coins_balance += number_of_hours
        current_user.sullivan_coins_balance -= number_of_hours
        job_performed_by.save()
        current_user.save()
        return redirect('dashboard:dashboard_home')
    else:
        return redirect('pages:home')


@login_required
def complete_job(request, response_id):
    rsp = get_object_or_404(TaskResponse, pk=response_id)

    if request.method == 'GET':
        context = {
            'response_id': response_id,
            'job_title': rsp.task.title,
            'job_user': f'{rsp.created_by.first_name} {rsp.created_by.last_name}',
            'max_hours': rsp.recipient.sullivan_coins_balance
        }
        return render(request, 'dashboard/dashboard_task_complete_job.html', context)
    elif request.method == 'POST':
        # number_of_hours = float(request.POST.get('numberOfHours'))
        rating = float(request.POST.get('rating'))
        comments = request.POST.get('comments')

        job_performed_by = rsp.created_by
        current_user = request.user

        review = UserReview(rating=rating, comments=comments, reviewee=job_performed_by, author=current_user)

        rsp.status = TaskResponse.COMPLETED
        rsp.resolved_on = datetime.datetime.now()

        review.save()
        rsp.save()

        return redirect('dashboard:dashboard_home')
    else:
        return redirect('pages:home')


class UserMessages(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard_user_messages.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_id = self.request.GET.get('job-id') or ''
        sender_id = self.request.GET.get('sender') or ''
        context['job_id'] = job_id
        context['sender_id'] = sender_id
        return context


class UserMessageThread(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard_message_thread.html'
