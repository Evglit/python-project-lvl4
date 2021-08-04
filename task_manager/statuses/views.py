from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Statuses


class StatusesPage(ListView):
    """Class for creating a status page."""
    model = Statuses
    template_name = 'statuses.html'
    context_object_name = 'statuses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cтатусы'
        return context


class CreateStatus(CreateView):
    pass


class UpdateStatus(UpdateView):
    pass


class DeleteStatus(DeleteView):
    pass
