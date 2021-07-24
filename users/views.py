from django.views.generic import DetailView, UpdateView
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Avg
from django.shortcuts import render

from tasks.models import Task, TaskResponse
from reviews.models import UserReview

CustomUser = get_user_model()


@login_required
def user_list(request):
    users = CustomUser.objects.filter(is_staff=False, is_superuser=False)

    for user in users:
        user.average_rating = UserReview.objects.filter(reviewee=user).aggregate(Avg('rating'))['rating__avg']

    context = {
        'customuser_list': users,
    }

    return render(request, 'users/customuser_list.html', context)


class UserDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total_user_jobs = len(Task.objects.filter(created_by=self.object.id))
        user_reviews = UserReview.objects.filter(reviewee=self.object.id)
        average_rating = user_reviews.aggregate(Avg('rating'))['rating__avg']
        context['total_user_jobs'] = total_user_jobs
        context['user_reviews'] = user_reviews
        context['average_rating'] = average_rating
        return context


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomUser
    fields = [
        'first_name', 'last_name', 'username', 'date_of_birth', 'biography', 'skill_categories', 'skills', 
        'social_facebook', 'social_twitter', 'social_instagram', 'social_linkedin', 'profile_pic',
    ]
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name_suffix = '_update_form'

    def test_func(self):
        obj = self.get_object()
        return obj == self.request.user


# class UserDashboardView(LoginRequiredMixin, TemplateView):
#     template_name = 'users/customuser_dashboard.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user_jobs = Task.objects.filter(
#             created_by=self.request.user,
#             status=Task.AVAILABLE
#         ).order_by('expires_on')

#         pending_responses = TaskResponse.objects.filter(
#             recipient=self.request.user,
#             status=TaskResponse.PENDING
#         ).order_by('created_by')

#         accepted_responses = TaskResponse.objects.filter(
#             recipient=self.request.user,
#             status=TaskResponse.ACCEPTED
#         )

#         sent_responses = TaskResponse.objects.filter(
#             created_by=self.request.user
#         )

#         context['user_jobs'] = user_jobs
#         context['pending_responses'] = pending_responses
#         context['accepted_responses'] = accepted_responses
#         context['sent_responses'] = sent_responses

#         return context


# class UserMessages(LoginRequiredMixin, TemplateView):
#     template_name = 'users/customuser_messages.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     user_messages = Response.objects.filter(recipient=self.request.user)
    #     context['user_messages'] = user_messages
    #     return context
