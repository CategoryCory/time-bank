from django.urls import path

from . import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.UserDashboardView.as_view(), name='dashboard_home'),
    path('pending-responses/', views.PendingResponsesView.as_view(), name='dashboard_pending_responses'),
    path('accepted-responses/', views.AcceptedResponsesView.as_view(), name='dashboard_accepted_responses'),
    path('completed-responses/', views.CompletedResponsesView.as_view(), name='dashboard_completed_responses'),
    path('sent-responses/', views.SentResponsesView.as_view(), name='dashboard_sent_responses'),
    path('new-task/', views.TaskCreateView.as_view(), name='new_task'),
    path('task/edit/<int:pk>/', views.TaskUpdateView.as_view(), name='task_update'),
    path('task/delete/<int:pk>/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('record-time/<int:response_id>/', views.record_time, name='record_time'),
    path('complete-job/<int:response_id>/', views.complete_job, name='complete_job'),
    path('<str:username>/edit/', views.UserUpdateView.as_view(), name='user_update'),
    path('messages/', views.UserMessages.as_view(), name='user_messages'),
    path('messages/thread/', views.UserMessageThread.as_view(), name='user_message_thread'),
]