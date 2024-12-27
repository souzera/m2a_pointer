from django.contrib import admin

from .models import *

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    pass

@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    pass

@admin.register(Ponto)
class PontoAdmin(admin.ModelAdmin):
    pass