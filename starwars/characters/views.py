from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView

from characters import ops
from characters.models import Collection


class FetchCollection(View):
    def get(self, request):
        Collection.objects.fetch_and_create()
        url = reverse("collections")
        return HttpResponseRedirect(url)


class CollectionList(ListView):
    model = Collection
    ordering = ["-created"]


class CollectionDetail(DetailView):
    model = Collection

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        limit = int(self.request.GET.get("limit", 10))
        table_data = ops.load_table(self.object, limit)

        context.update(
            {
                "header": table_data.header,
                "data": table_data.data,
                "next_limit": table_data.next_limit,
            }
        )
        return context
