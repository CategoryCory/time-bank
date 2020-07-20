from django.urls import path

# from .views import UserListView, UserDetailView, UserUpdateView
from . import views

app_name = 'users'
urlpatterns = [
    path('', views.UserListView.as_view(), name='user_list'),
    # path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('dashboard/', views.UserDashboardView.as_view(), name='user_dashboard'),
    path('<slug:username>/', views.UserDetailView.as_view(), name='user_detail'),
    path('<slug:username>/edit/', views.UserUpdateView.as_view(), name='user_update'),
]
