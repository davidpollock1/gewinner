from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from .forms import UserRegisterForm, UserSettingsForm
from .models import CustomUser
from django.contrib import messages

class RegisterView(CreateView):
    model = CustomUser
    form_class = UserRegisterForm
    template_name = 'userAuth/register.html'
    success_url = reverse_lazy('login')
    
    def form_invalid(self, form):
        return super().form_invalid(form)

class LoginView(LoginView):
    template_name = "userAuth/login.html"
    redirect_authenticated_user = True

class LogoutView(LogoutView):
    success_url = reverse_lazy('login')
    
class UserSettingsView(UpdateView):
    model = CustomUser
    form_class = UserSettingsForm
    template_name = 'userAuth/user_settings.html'
    success_url = reverse_lazy('user_settings')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Your settings have been updated successfully!")
        return super().form_valid(form)
