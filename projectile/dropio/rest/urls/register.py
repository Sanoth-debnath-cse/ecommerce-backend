from django.urls import path

from dropio.rest.views.register import DropUserCreateView

urlpatterns = [
    path("/onboarding", DropUserCreateView.as_view(), name="dropio.user-list")
]
