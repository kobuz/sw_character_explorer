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

    def get_context_data(self, **kwargs):
        context = super(CollectionDetail, self).get_context_data(**kwargs)
        table = ops.load_table(self.object)
        limit = int(self.request.GET.get("limit", 10))
        import petl

        context.update(
            {
                "characters": table,
                "limit": limit,
                "header": petl.header(table),
                "data": petl.data(table, limit),
                "next_limit": limit + 10 if limit < table.len() else None,
            }
        )
        return context
