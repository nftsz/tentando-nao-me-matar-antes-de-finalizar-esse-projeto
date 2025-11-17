from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.shortcuts import render
from .forms import LoginForm

class CustomLoginView(LoginView):
    template_name = 'usuarios/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

def home(request):
    return render(request, 'usuarios/home.html', {'user': request.user})

