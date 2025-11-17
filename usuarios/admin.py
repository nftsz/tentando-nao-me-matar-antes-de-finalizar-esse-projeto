from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, ProfissionalExecutante, UBS

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
            'fields': ('cpf', 'nome', 'sobrenome', 'email', 'ubs', 'cargo', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )

    search_fields = ('cpf', 'nome', 'email')
    ordering = ('cpf',)


@admin.register(UBS)
class UBSAdmin(admin.ModelAdmin):
    list_display = ('nome', 'codigo', 'regional', 'telefone')
    search_fields = ('nome', 'codigo', 'regional')


@admin.register(ProfissionalExecutante)
class ProfissionalExecutanteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'especialidade')
    search_fields = ('nome', 'especialidade')
