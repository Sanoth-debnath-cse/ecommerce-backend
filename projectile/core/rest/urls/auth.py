from django.urls import path

from core.rest.views.auth import UserRegistrationView

urlpatterns = [
    path("onboarding", UserRegistrationView.as_view(), name="user.onboarding")
]
