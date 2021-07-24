from django.urls import path, re_path

from . import views

app_name = 'tasks'
urlpatterns = [
    path('', views.task_list, name='task_list'),
    re_path(r'category/(?:(?P<slug>[a-zA-Z0-9-]+)/)?$', views.task_list, name='task_list'),
    path('<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('task-response/', views.task_response, name='task_response'),
    path('update-response-status/<int:response_id>/<str:new_status>/', views.update_response_status, name='update_response_status'),
]
