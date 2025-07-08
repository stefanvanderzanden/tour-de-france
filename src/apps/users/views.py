from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import TemplateView

from .forms import CustomUserCreationForm, CustomAuthenticationForm
from ..races.models import Round


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = "users/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("dashboard")


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "users/signup.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return redirect("dashboard")


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("login")


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "users/dashboard.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        available_rounds = Round.objects.all()
        active_rounds = Round.objects.filter(participantteam__user=self.request.user).order_by("start_date")
        context_data = super().get_context_data(**kwargs)
        context_data.update({
            "available_rounds": available_rounds,
            "active_rounds": active_rounds,
        })
        return context_data