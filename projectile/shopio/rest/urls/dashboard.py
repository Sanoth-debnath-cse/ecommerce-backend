from django.urls import path

from shopio.rest.views.dashboard import PrivateDashboardView

urlpatterns = [
    path("", PrivateDashboardView.as_view(), name="private.dashboard-details")
]
