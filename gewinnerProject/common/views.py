from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = "common/home.html"

    def get_template_names(self):
        if self.request.user.is_authenticated:
            return ["common/dashboard.html"]
        else:
            return [self.template_name]