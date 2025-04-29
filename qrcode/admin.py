from django.contrib import admin
from .models import Cliente, ClienteQtd


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('cpf', 'cnpj', 'nome', 'razsoc', 'checkin', 'data_hora')
    search_fields = ('cpf', 'cnpj', 'nome', 'razsoc')
    list_filter = ('checkin',)
    ordering = ('cpf',)
    fieldsets = (
        (None, {
            'fields': ('cpf', 'cnpj', 'razsoc', 'nome', 'checkin', 'data_hora')
        }),
    )


@admin.register(ClienteQtd)
class ClienteQtdAdmin(admin.ModelAdmin):
    list_display = ('cnpj', 'razsoc', 'email', 'qtd_convites')
    search_fields = ('cnpj',)
    ordering = ('cnpj',)
    fieldsets = (
        (None, {
            'fields': ('cnpj', 'razsoc', 'email', 'qtd_convites')
        }),
    )
