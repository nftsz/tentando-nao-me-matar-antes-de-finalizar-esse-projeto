from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import Usuario, ProfissionalExecutante, UBS, Paciente, OCI


# ===========================
# USUARIO
# ===========================
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ('cpf', 'nome', 'sobrenome', 'email', 'cargo', 'ubs', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'ubs', 'cargo')

    fieldsets = (
        (None, {'fields': ('cpf', 'password')}),
        ('Informações pessoais', {'fields': ('nome', 'sobrenome', 'email', 'ubs', 'cargo')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'cpf', 'nome', 'sobrenome', 'email', 'ubs', 'cargo',
                'password1', 'password2', 'is_active', 'is_staff'
            )
        }),
    )

    search_fields = ('cpf', 'nome', 'email')
    ordering = ('cpf',)



# ===========================
# UBS
# ===========================
@admin.register(UBS)
class UBSAdmin(admin.ModelAdmin):
    list_display = ('nome', 'codigo', 'regional', 'telefone')
    search_fields = ('nome', 'codigo', 'regional')



# ===========================
# PROFISSIONAL EXECUTANTE
# ===========================
@admin.register(ProfissionalExecutante)
class ProfissionalExecutanteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'especialidade')
    search_fields = ('nome', 'especialidade')



# ===========================
# OCI INLINE (para PACIENTE)
# ===========================
class OCIInline(admin.TabularInline):
    model = OCI
    extra = 1
    fields = ('codigo_oci', 'nome_oci', 'tipo', 'data_abertura', 'data_conclusao')



# ===========================
# PACIENTE
# ===========================
@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = (
        'nome_completo',
        'cpf',
        'telefone',
        'ubs_solicitante',
        'codigo_sisreg',
        'data_registro_display'
    )
    search_fields = ('nome_completo', 'cpf', 'codigo_sisreg')
    list_filter = ('ubs_solicitante', 'data_registro')
    ordering = ('-data_registro',)

    inlines = [OCIInline]

    # Deixa a data bonita
    def data_registro_display(self, obj):
        return obj.data_registro.strftime("%d/%m/%Y %H:%M")
    data_registro_display.short_description = "Data de Registro"



# ===========================
# OCI
# ===========================
@admin.register(OCI)
class OCIAdmin(admin.ModelAdmin):
    list_display = (
        'codigo_oci',
        'nome_oci',
        'paciente',
        'tipo',
        'data_abertura',
        'data_limite',
        'status_atraso',
        'data_conclusao',
    )
    search_fields = ('codigo_oci', 'nome_oci', 'paciente__nome_completo', 'paciente__cpf')
    list_filter = ('tipo', 'data_abertura')
    ordering = ('data_abertura',)

    readonly_fields = ('data_limite', 'status_atraso')

    def status_atraso(self, obj):
        if obj.atrasada:
            return format_html('<span style="color:red; font-weight:bold;">ATRASADA</span>')
        return format_html('<span style="color:green; font-weight:bold;">Dentro do prazo</span>')
    status_atraso.short_description = "Status"
