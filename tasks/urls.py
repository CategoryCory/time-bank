from django.urls import path

from .views import TaskRequestListView, TaskRequestDetailView, TaskRequestUpdateView

app_name = 'tasks'
urlpatterns = [
    path('requests/', TaskRequestListView.as_view(), name='task_request_list'),
    path('requests/<int:pk>/', TaskRequestDetailView.as_view(), name='task_request_detail'),
    path('requests/<int:pk>/edit/', TaskRequestUpdateView.as_view(), name='task_request_update'),
]
