from django.urls import path
from apps.races.views import TestView

app_name = "races"

urlpatterns = [
    path("races/", TestView.as_view(), name="list"),
]
