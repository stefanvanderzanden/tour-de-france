from django.views.generic import TemplateView


class TestView(TemplateView):
    template_name = "users/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["range_iterator"] = range(1, 28)
        return context


