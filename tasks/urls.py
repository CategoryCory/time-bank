from django.urls import path, re_path

from . import views

app_name = 'tasks'
urlpatterns = [
    path('', views.task_list, name='task_list'),
    re_path(r'category/(?:(?P<slug>[a-zA-Z0-9-]+)/)?$', views.task_list, name='task_list'),
    path('new/', views.TaskCreateView.as_view(), name='task_new'),
    path('<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('<int:pk>/edit/', views.TaskUpdateView.as_view(), name='task_update'),
    path('<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('task-response/', views.task_response, name='task_response'),
    path('update-response-status/<int:response_id>/<str:new_status>/', views.update_response_status, name='update_response_status'),
    # path('deny-response/<int:response_id>/', views.deny_response, name='deny_response'),
    path('record-time/<int:response_id>/', views.record_time, name='record_time'),
    path('complete-job/<int:response_id>/', views.complete_job, name='complete_job'),
]
