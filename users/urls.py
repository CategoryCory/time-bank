from django.urls import path

from .views import UserListView, UserDetailView, UserUpdateView


urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    path('<slug:username>/', UserDetailView.as_view(), name='user_detail'),
    path('<slug:username>/edit', UserUpdateView.as_view(), name='user_update'),
]