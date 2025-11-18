from django.urls import path
from .views import CustomLoginView, CustomLogoutView, home, buscar_paciente, cadastrar_oci, consulta_oci
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('', login_required(home), name='home'),
    path("buscar-paciente/", login_required(buscar_paciente), name="buscar_paciente"),
    path("cadastrar-oci/", login_required(cadastrar_oci), name="cadastrar_oci"),
    path("consulta/", login_required(consulta_oci), name="consulta_oci"),
]