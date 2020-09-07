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
        table_data = ops.load_table_data(self.object, limit)

        context.update(
            {
                "header": table_data.header,
                "data": table_data.data,
                "next_limit": table_data.next_limit,
            }
        )
        return context


class ValueCount(DetailView):
    model = Collection
    template_name = "characters/value_count.html"

    @property
    def selected_headers(self):
        group_by = self.request.GET.get("groupby", "")
        if group_by:
            return group_by.split(",")
        else:
            return []

    def get(self, request, *args, **kwargs):
        selected = self.selected_headers
        add = request.GET.get("add")
        remove = request.GET.get("remove")
        if add:
            return self.redirect_to_value_count(selected + [add])
        elif remove:
            selected = set(selected) - {remove}
            if selected:
                return self.redirect_to_value_count(selected)
            else:
                url = reverse(
                    "collection-detail", args=[self.kwargs.get(self.pk_url_kwarg)]
                )
                return HttpResponseRedirect(url)
        return super().get(request, *args, **kwargs)

    def redirect_to_value_count(self, selected):
        joined = ",".join(sorted(set(selected)))
        url = reverse("value-count", args=[self.kwargs.get(self.pk_url_kwarg)])
        return HttpResponseRedirect(f"{url}?groupby={joined}")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        table = ops.load_grouped_data(self.object, self.selected_headers)
        context.update(
            {
                "group_by": self.request.GET.get("groupby", ""),
                "selected": set(self.selected_headers),
                "header": table.header,
                "data": table.data,
            }
        )
        return context
