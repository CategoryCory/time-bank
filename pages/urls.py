from django.urls import path

from .views import HomePageView, BrowseUsersView

app_name = 'pages'
urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('browse-users/', BrowseUsersView.as_view(), name='browse_users'),
]