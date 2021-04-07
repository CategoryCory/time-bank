from django.urls import path

from . import views

app_name = 'tasks'
urlpatterns = [
    path('', views.TaskListView.as_view(), name='task_list'),
    path('new/', views.TaskCreateView.as_view(), name='task_new'),
    path('<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('<int:pk>/edit/', views.TaskUpdateView.as_view(), name='task_update'),
    path('<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('task-response/', views.task_response, name='task_response'),
    path('accept-response/<int:response_id>/', views.accept_response, name='accept_response'),
    path('deny-response/<int:response_id>/', views.deny_response, name='deny_response'),
    path('record-time/<int:response_id>/', views.record_time, name='record_time'),
    path('complete-job/<int:response_id>/', views.complete_job, name='complete_job'),
]
