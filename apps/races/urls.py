from django.urls import path
from apps.races.views import TestView, AjaxView

app_name = "races"

urlpatterns = [
    path("races/", TestView.as_view(), name="list"),
    path("ajax/", AjaxView.as_view(), name="ajax")
]
