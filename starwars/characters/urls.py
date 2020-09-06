from django.urls import path
from django.views.generic import RedirectView

from characters.views import CollectionList, FetchCollection, CollectionDetail

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="collections")),
    path("collections/", CollectionList.as_view(), name="collections"),
    path("collection/<int:pk>/", CollectionDetail.as_view(), name="collection-detail"),
    path("fetch-collection/", FetchCollection.as_view(), name="fetch-collection"),
]
