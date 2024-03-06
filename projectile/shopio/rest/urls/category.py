from django.urls import path

from shopio.rest.views.category import (
    PrivateCategoryListView,
    PrivateCategoryDetailView,
)

urlpatterns = [
    path(
        "/<uuid:category_uid>",
        PrivateCategoryDetailView.as_view(),
        name="private.category-details",
    ),
    path("", PrivateCategoryListView.as_view(), name="private.category-list"),
]
