from django.urls import path

from core.rest.views.auth import UserRegistrationView, UserLoginView

urlpatterns = [
    path("token", UserLoginView.as_view(), name="user.token"),
    path("onboarding", UserRegistrationView.as_view(), name="user.onboarding"),
]
