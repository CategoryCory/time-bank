from django.views.generic import ListView, DetailView, UpdateView

from .models import Request, Offer


class TaskRequestListView(ListView):
    model = Request
    paginate_by = 25
    template_name = 'tasks/requests/request_list.html'


class TaskRequestDetailView(DetailView):
    model = Request
    template_name = 'tasks/requests/request_detail.html'


class TaskRequestUpdateView(UpdateView):
    model = Request
    fields = ['title', 'description', 'expires', 'status', 'categories', ]
    template_name = 'tasks/requests/request_update_form.html'
