from django.urls import path

from . import views

app_name = 'pages'
urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('terms-of-service/', views.TermsView.as_view(), name='terms'),
    path('privacy-policy/', views.PrivacyPolicyView.as_view(), name='privacy-policy'),
    # path('browse-users/', BrowseUsersView.as_view(), name='browse_users'),
]