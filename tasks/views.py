from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.conf import settings

from .models import Task, Response
from reviews.models import UserReview


class TaskListView(ListView):
    model = Task
    # queryset = Task.objects.filter(task_type='REQUEST', status='AVAILABLE')
    paginate_by = 25

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['task_type'] = 'requests'
    #     return context


# class TaskOfferListView(ListView):
#     model = Task
#     queryset = Task.objects.filter(task_type='OFFER', status='AVAILABLE')
#     paginate_by = 25
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['task_type'] = 'offers'
#         return context
#
#
class TaskDetailView(DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'expires_on', 'frequency', ]
    template_name_suffix = '_create_form'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['task_type'] = 'request'
    #     return context
    #
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        # form.instance.task_type = 'REQUEST'
        return super().form_valid(form)


# class TaskOfferCreateView(LoginRequiredMixin, CreateView):
#     model = Task
#     fields = ['title', 'description', 'expires_on', 'frequency', ]
#     template_name_suffix = '_create_form'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['task_type'] = 'offer'
#         return context
#
#     def form_valid(self, form):
#         form.instance.created_by = self.request.user
#         form.instance.task_type = 'OFFER'
#         return super().form_valid(form)
#
#
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
        # if obj.task_type == 'REQUEST':
        #     return reverse_lazy('tasks:task_request_list')
        # else:
        #     return reverse_lazy('tasks:task_offer_list')
        return reverse_lazy('users:user_dashboard')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.soft_delete()
        return HttpResponseRedirect(self.get_success_url())


@login_required
def task_response(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        message = request.POST.get('message')

        user = request.user

        if not user.is_approved:
            return redirect('pages:home')

        task = get_object_or_404(Task, pk=task_id)

        response = Response(task=task, message=message, created_by=user, recipient=task.created_by)
        response.save()

        # Send email
        email_subject = 'Sullivan Foundation Time Bank Response'
        email_body = (
            f'You have a response from one of your job listings on the Sullivan Time Bank.\n'
            f'Job: {task}\n'
            f'From user: {user.first_name} {user.last_name}\n'
            f'Message: {message}'
        )
        send_mail(
            email_subject,
            email_body,
            settings.DEFAULT_FROM_EMAIL,
            [task.created_by.email],
            fail_silently=True
        )

        # if task.task_type == 'REQUEST':
        #     return_url = 'tasks:task_request_list'
        # else:
        #     return_url = 'tasks:task_offer_list'

        # return redirect(return_url)
        return redirect('tasks:task_list')
    else:
        return redirect('pages:home')


@login_required
def accept_response(request, response_id):
    rsp = get_object_or_404(Response, pk=response_id)

    if request.user != rsp.task.created_by:
        return redirect('pages:home')

    rsp.status = Response.ACCEPTED
    rsp.save()
    return redirect('users:user_dashboard')


@login_required
def deny_response(request, response_id):
    rsp = get_object_or_404(Response, pk=response_id)

    if request.user != rsp.task.created_by:
        return redirect('pages:home')

    rsp.status = Response.DECLINED
    rsp.save()
    return redirect('users:user_dashboard')


@login_required
def record_time(request, response_id):
    rsp = get_object_or_404(Response, pk=response_id)

    if request.method == 'GET':
        context = {
            'response_id': response_id,
            'job_title': rsp.task.title,
            'job_user': f'{rsp.created_by.first_name} {rsp.created_by.last_name}',
            'max_hours': rsp.recipient.sullivan_coins_balance
        }
        return render(request, 'tasks/task_record_time.html', context)
    elif request.method == 'POST':
        number_of_hours = float(request.POST.get('numberOfHours'))
        job_performed_by = rsp.created_by
        current_user = request.user
        job_performed_by.sullivan_coins_balance += number_of_hours
        current_user.sullivan_coins_balance -= number_of_hours
        job_performed_by.save()
        current_user.save()
        return redirect('users:user_dashboard')
    else:
        return redirect('pages:home')


@login_required
def complete_job(request, response_id):
    rsp = get_object_or_404(Response, pk=response_id)

    if request.method == 'GET':
        context = {
            'response_id': response_id,
            'job_title': rsp.task.title,
            'job_user': f'{rsp.created_by.first_name} {rsp.created_by.last_name}',
            'max_hours': rsp.recipient.sullivan_coins_balance
        }
        return render(request, 'tasks/task_complete_job.html', context)
    elif request.method == 'POST':
        number_of_hours = float(request.POST.get('numberOfHours'))
        rating = float(request.POST.get('rating'))
        comments = request.POST.get('comments')

        job_performed_by = rsp.created_by
        current_user = request.user

        review = UserReview(rating=rating, comments=comments, reviewee=job_performed_by, author=current_user)

        job_performed_by.sullivan_coins_balance += number_of_hours
        current_user.sullivan_coins_balance -= number_of_hours

        rsp.status = Response.COMPLETED

        job_performed_by.save()
        current_user.save()
        review.save()
        rsp.save()

        return redirect('users:user_dashboard')
    else:
        return redirect('pages:home')
