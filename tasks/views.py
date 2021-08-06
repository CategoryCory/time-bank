from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Avg
from django.shortcuts import render, redirect, get_object_or_404

from .models import Task, TaskCategory, TaskResponse, TaskAvailability
from user_messages.models import UserMessageThread, UserMessage
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            current_response = TaskResponse.objects.filter(task=self.object, created_by=self.request.user).first()
        else:
            current_response = None

        availabilities = TaskAvailability.objects.filter(task=self.object)
        user_reviews = UserReview.objects.filter(reviewee=self.object.created_by)
        average_rating = user_reviews.aggregate(Avg('rating'))['rating__avg']
        context['availabilities'] = availabilities
        context['average_rating'] = average_rating
        context['current_response'] = current_response
        return context


@login_required
def task_response(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        message = request.POST.get('message')

        user = request.user

        if not user.is_approved:
            return redirect('pages:home')

        task = get_object_or_404(Task, pk=task_id)

        # Save response on dashboard
        response = TaskResponse(task=task, created_by=user, recipient=task.created_by)
        response.save()

        # Create message
        user_message_thread = UserMessageThread(created_by=user, recipient=task.created_by, job=task)
        user_message_thread.save()

        user_message = UserMessage(sender=user, recipient=task.created_by, message_body=message, thread=user_message_thread)
        user_message.save()

        # Send email
        email_subject = 'Sullivan Foundation Time Bank Response'
        email_body = (
            f'You have a response to your job listing "{task}" on the Sullivan Time Bank.\n'
            f'To view this message, please log into your account at https://sullivantimebank.org/accounts/login/ \n'
            f'Please do not reply to this email.\n'
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
