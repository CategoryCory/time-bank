from django.urls import path

# from .views import UserListView, UserDetailView, UserUpdateView
from . import views

app_name = 'users'
urlpatterns = [
    # path('', views.UserListView.as_view(), name='user_list'),
    path('', views.user_list, name='user_list'),
    # path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('dashboard/', views.UserDashboardView.as_view(), name='user_dashboard'),
    # path('dashboard/messages/', views.UserMessageListView.as_view(), name='user_message_list'),
    # path('dashboard/messages/<int:pk>/', views.UserMessageDetailView.as_view(), name='user_message_detail'),
    path('<str:username>/', views.UserDetailView.as_view(), name='user_detail'),
    path('<str:username>/edit/', views.UserUpdateView.as_view(), name='user_update'),
]
