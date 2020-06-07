from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy

from .models import Request, Offer

""" TASK-REQUEST VIEWS """


class TaskRequestListView(ListView):
    model = Request
    paginate_by = 25
    template_name = 'tasks/requests/request_list.html'


class TaskRequestCreateView(CreateView):
    model = Request
    fields = ['title', 'description', 'expires', ]
    template_name = 'tasks/requests/request_new.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class TaskRequestDetailView(DetailView):
    model = Request
    template_name = 'tasks/requests/request_detail.html'


class TaskRequestUpdateView(UpdateView):
    model = Request
    fields = ['title', 'description', 'expires', 'status', ]
    template_name = 'tasks/requests/request_update_form.html'


class TaskRequestDeleteView(DeleteView):
    model = Request
    success_url = reverse_lazy('tasks:task_request_list')
    template_name = 'tasks/requests/request_confirm_delete.html'


""" TASK-OFFER VIEWS """


class TaskOfferListView(ListView):
    model = Offer
    paginate_by = 25
    template_name = 'tasks/offers/offer_list.html'


class TaskOfferCreateView(CreateView):
    model = Offer
    fields = ['title', 'description', 'expires', ]
    template_name = 'tasks/offers/offer_new.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class TaskOfferDetailView(DetailView):
    model = Offer
    template_name = 'tasks/offers/offer_detail.html'


class TaskOfferUpdateView(UpdateView):
    model = Offer
    fields = ['title', 'description', 'expires', 'status', ]
    template_name = 'tasks/offers/offer_update_form.html'


class TaskOfferDeleteView(DeleteView):
    model = Offer
    success_url = reverse_lazy('tasks:task_offer_list')
    template_name = 'tasks/offers/offer_confirm_delete.html'
