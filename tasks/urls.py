from django.urls import path

from . import views

app_name = 'tasks'
urlpatterns = [
    path('requests/', views.TaskRequestListView.as_view(), name='task_request_list'),
    path('requests/new-request/', views.TaskRequestCreateView.as_view(), name='task_request_create'),
    path('requests/<int:pk>/', views.TaskRequestDetailView.as_view(), name='task_request_detail'),
    path('requests/<int:pk>/edit/', views.TaskRequestUpdateView.as_view(), name='task_request_update'),
    path('offers/', views.TaskOfferListView.as_view(), name='task_offer_list'),
    path('offers/new-offer/', views.TaskOfferCreateView.as_view(), name='task_offer_create'),
    path('offers/<int:pk>/', views.TaskOfferDetailView.as_view(), name='task_offer_detail'),
    path('offers/<int:pk>/edit/', views.TaskOfferUpdateView.as_view(), name='task_offer_update'),
]