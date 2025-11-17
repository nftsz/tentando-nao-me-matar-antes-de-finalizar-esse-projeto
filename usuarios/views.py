from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .forms import LoginForm, PacienteForm, OCIForm
from django.http import JsonResponse
from .models import Paciente


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

def buscar_paciente(request):
    cpf = request.GET.get('cpf')
    try:
        p = Paciente.objects.get(cpf=cpf)
        return JsonResponse({
            "exists": True,
            "dados": {
                "nome": p.nome_completo,
                "cpf": p.cpf,
                "telefone": p.telefone,
                "codigo_sisreg": p.codigo_sisreg,
                "ubs": p.ubs_solicitante_id,
                "data_agendamento": p.data_agendamento_sisreg,
                "id": p.id,
            }
        })
    except Paciente.DoesNotExist:
        return JsonResponse({"exists": False})
    
def cadastrar_oci(request):
    if request.method == "POST":
        paciente_id = request.POST.get("paciente_id")

        # Paciente já existe
        if paciente_id:
            paciente = Paciente.objects.get(id=paciente_id)
            paciente_form = PacienteForm(request.POST, instance=paciente)
        else:
            paciente_form = PacienteForm(request.POST)

        oci_form = OCIForm(request.POST)

        if paciente_form.is_valid() and oci_form.is_valid():
            paciente = paciente_form.save()
            oci = oci_form.save(commit=False)
            oci.paciente = paciente
            oci.save()

            return redirect("home")  # troque pela sua página final

    else:
        paciente_form = PacienteForm()
        oci_form = OCIForm()

    return render(request, "usuarios/cadastro_oci.html", {
        "paciente_form": paciente_form,
        "oci_form": oci_form
    })
