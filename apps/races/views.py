from django.views.generic import TemplateView


class TestView(TemplateView):
    template_name = "theme/layouts/authenticated/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["range_iterator"] = range(1, 28)
        return context


class AjaxView(TemplateView):
    template_name = "theme/layouts/authenticated/ajax.html"

    # def dispatch(self, request, *args, **kwargs):
    #     print("TESTING")
    #     return super().dispatch(request, args, kwargs)
