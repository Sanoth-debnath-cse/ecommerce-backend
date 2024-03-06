from django.urls import path

from core.rest.views.me import PublicMeView

urlpatterns = [path("", PublicMeView.as_view(), name="public-me")]
