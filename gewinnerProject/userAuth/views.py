from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

class LoginView(LoginView):
    template_name = "login.html"
    redirect_authenticated_user = True

class LogoutView(LogoutView):
    success_url = reverse_lazy('login')
