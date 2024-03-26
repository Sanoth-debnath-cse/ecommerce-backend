from django.urls import include, path

urlpatterns = [
    path("", include("dropio.rest.urls.register")),
]
