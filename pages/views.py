from django.views.generic import TemplateView, ListView
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class HomePageView(TemplateView):
    template_name = 'pages/home.html'


class BrowseUsersView(ListView):
    model = CustomUser
    template_name = 'pages/browse_users.html'
