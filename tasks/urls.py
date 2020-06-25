from django.urls import path

from . import views

app_name = 'tasks'
urlpatterns = [
    path('requests/', views.TaskRequestListView.as_view(), name='task_request_list'),
    path('offers/', views.TaskOfferListView.as_view(), name='task_offer_list'),
    path('requests/new/', views.TaskRequestCreateView.as_view(), name='task_request_new'),
    path('offers/new/', views.TaskOfferCreateView.as_view(), name='task_offer_new'),
    path('<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('<int:pk>/edit/', views.TaskUpdateView.as_view(), name='task_update'),
    path('<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('task-response/', views.task_response, name='task_response'),
]
