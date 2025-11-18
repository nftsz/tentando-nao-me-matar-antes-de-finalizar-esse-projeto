from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .forms import LoginForm, PacienteForm, OCIForm
from django.http import JsonResponse
from .models import Paciente, OCI

class CustomLoginView(LoginView):
    template_name = 'usuarios/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')


def home(request):
    # Todas as OCIs
    oci_queryset = OCI.objects.select_related("paciente").order_by("-data_abertura")
    paginator_latest = Paginator(oci_queryset, 5)
    page_latest = request.GET.get("page_latest", 1)
    latest_page = paginator_latest.get_page(page_latest)

    # OCIs atrasadas (usando a property atrasada)
    vencidas_queryset = OCI.objects.select_related("paciente").filter(
        data_conclusao__isnull=True
    ).order_by("data_abertura")

    paginator_vencidas = Paginator(vencidas_queryset, 5)
    page_vencidas = request.GET.get("page_vencidas", 1)
    vencidas_page = paginator_vencidas.get_page(page_vencidas)

    return render(request, "usuarios/home.html", {
        "latest_page": latest_page,
        "vencidas_page": vencidas_page,
    })


def buscar_paciente(request):
    cpf = request.GET.get('cpf')
    if not cpf:
        return JsonResponse({"exists": False})

    cpf_normalizado = cpf.replace(".", "").replace("-", "")
    try:
        p = Paciente.objects.get(cpf=cpf_normalizado)
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
            return redirect("home")

    else:
        paciente_form = PacienteForm()
        oci_form = OCIForm()

    return render(request, "usuarios/cadastro_oci.html", {
        "paciente_form": paciente_form,
        "oci_form": oci_form
    })


def buscar_ocis(request):
    cpf = request.GET.get("cpf")
    if not cpf:
        return JsonResponse({"exists": False, "erro": "Digite um CPF antes de buscar."})

    cpf_normalizado = cpf.replace(".", "").replace("-", "")

    try:
        paciente = Paciente.objects.get(cpf=cpf_normalizado)
        ocis = paciente.ocis.select_related("profissional_executante").all()

        dados_ocis = []
        for oci in ocis:
            dados_ocis.append({
                "codigo": oci.codigo_oci,
                "nome": oci.nome_oci,
                "tipo": oci.get_tipo_display(),
                "medico": str(oci.profissional_executante),
                "abertura": oci.data_abertura.strftime("%d/%m/%Y") if oci.data_abertura else "",
                "conclusao": oci.data_conclusao.strftime("%d/%m/%Y") if oci.data_conclusao else "",
                "limite": oci.data_limite.strftime("%d/%m/%Y") if oci.data_limite else "",
                "atrasada": oci.atrasada,
            })

        return JsonResponse({
            "exists": True,
            "paciente": {
                "nome": paciente.nome_completo,
                "cpf": paciente.cpf_formatado,
            },
            "ocis": dados_ocis
        })

    except Paciente.DoesNotExist:
        return JsonResponse({"exists": False, "erro": "Paciente não encontrado."})


def consulta_oci(request):
    return render(request, "usuarios/consulta.html")
