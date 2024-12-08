from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = "common/home.html"

    def get_template_names(self):
        if self.request.user.is_authenticated:
            if self.request.user.user_type == 'admin':
                return ["common/dashboard.html"]
            if self.request.user.user_type == 'nurse':
                return ["common/dashboard_nurse.html"]
        else:
            return [self.template_name]
        
