from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView

from characters import ops
from characters.models import Collection


class FetchCollection(View):
    def get(self, request):
        ops.fetch_and_save()
        url = reverse("collections")
        return HttpResponseRedirect(url)


class CollectionList(ListView):
    model = Collection
    ordering = ["-created"]


class CollectionDetail(DetailView):
    model = Collection
