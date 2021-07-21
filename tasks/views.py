from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Avg
from django.shortcuts import render, redirect, get_object_or_404

from .models import Task, TaskCategory, TaskResponse
from reviews.models import UserReview


def task_list(request, slug=None):
    if slug is not None:
        category = TaskCategory.objects.get(slug=slug)
        tasks = Task.objects.filter(status=Task.AVAILABLE, categories=category).order_by('-expires_on')
        category_title = category.title
        category_description = category.description
    else:
        tasks = Task.objects.filter(status=Task.AVAILABLE).order_by('-expires_on')
        category_description = 'Search here to view all jobs posted. Use the menu in the header to view specific categories.'
        category_title = 'All Jobs'

    for task in tasks:
        user_average_review = UserReview.objects.filter(reviewee=task.created_by).aggregate(Avg('rating'))['rating__avg']
        task.user_average_review = user_average_review

    context = {
        'task_list': tasks,
        'category_title': category_title,
        'category_description': category_description,
    }
    return render(request, 'tasks/task_list.html', context)


class TaskDetailView(DetailView):
    model = Task


# class TaskCreateView(LoginRequiredMixin, CreateView):
#     model = Task
#     form_class = TaskForm
#     template_name_suffix = '_create_form'
#     success_url = reverse_lazy('tasks:task_list')

#     def get_context_data(self, **kwargs):
#         data = super(TaskCreateView, self).get_context_data(**kwargs)
#         if self.request.POST:
#             data['availabilities'] = TaskAvailabilityFormSet(self.request.POST)
#         else:
#             data['availabilities'] = TaskAvailabilityFormSet()
#         return data

#     def form_valid(self, form):
#         context = self.get_context_data()
#         availabilities = context['availabilities']
#         with transaction.atomic():
#             form.instance.created_by = self.request.user
#             self.object = form.save()
#             if availabilities.is_valid():
#                 availabilities.instance = self.object
#                 availabilities.save()
#         return super(TaskCreateView, self).form_valid(form)


# class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Task
#     fields = ['title', 'description', 'expires_on', 'status', ]
#     template_name_suffix = '_update_form'

#     def test_func(self):
#         obj = self.get_object()
#         return obj.created_by == self.request.user


# class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#     model = Task
#     template_name_suffix = '_confirm_delete'

#     def test_func(self):
#         obj = self.get_object()
#         return obj.created_by == self.request.user

#     def get_success_url(self):
#         # obj = self.get_object()
#         return reverse_lazy('users:user_dashboard')

#     def delete(self, request, *args, **kwargs):
#         obj = self.get_object()
#         obj.soft_delete()
#         return HttpResponseRedirect(self.get_success_url())


@login_required
def task_response(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        message = request.POST.get('message')

        user = request.user

        if not user.is_approved:
            return redirect('pages:home')

        task = get_object_or_404(Task, pk=task_id)

        response = TaskResponse(task=task, created_by=user, recipient=task.created_by)
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

        return redirect('tasks:task_list')
    else:
        return redirect('pages:home')


@login_required
def update_response_status(request, response_id, new_status):
    rsp = get_object_or_404(TaskResponse, pk=response_id)

    if request.user != rsp.task.created_by:
        return redirect('pages:home')

    rsp.status = getattr(TaskResponse, new_status)
    rsp.save()
    return redirect('dashboard:dashboard_home')


# @login_required
# def deny_response(request, response_id):
#     rsp = get_object_or_404(TaskResponse, pk=response_id)

#     if request.user != rsp.task.created_by:
#         return redirect('pages:home')

#     rsp.status = TaskResponse.DECLINED
#     rsp.save()
#     return redirect('users:user_dashboard')


# @login_required
# def record_time(request, response_id):
#     rsp = get_object_or_404(TaskResponse, pk=response_id)

#     if request.method == 'GET':
#         context = {
#             'response_id': response_id,
#             'job_title': rsp.task.title,
#             'job_user': f'{rsp.created_by.first_name} {rsp.created_by.last_name}',
#             'max_hours': rsp.recipient.sullivan_coins_balance
#         }
#         return render(request, 'tasks/task_record_time.html', context)
#     elif request.method == 'POST':
#         number_of_hours = float(request.POST.get('numberOfHours'))
#         job_performed_by = rsp.created_by
#         current_user = request.user
#         job_performed_by.sullivan_coins_balance += number_of_hours
#         current_user.sullivan_coins_balance -= number_of_hours
#         job_performed_by.save()
#         current_user.save()
#         return redirect('users:user_dashboard')
#     else:
#         return redirect('pages:home')


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

        rsp.status = TaskResponse.COMPLETED

        job_performed_by.save()
        current_user.save()
        review.save()
        rsp.save()

        return redirect('users:user_dashboard')
    else:
        return redirect('pages:home')
