from django.urls import path
from .views import CustomLoginView, CustomLogoutView, home, buscar_paciente, cadastrar_oci
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('', login_required(home), name='home'),
    path("buscar-paciente/", buscar_paciente, name="buscar_paciente"),
    path("cadastrar-oci/", cadastrar_oci, name="cadastrar_oci"),
]