from django.urls import path
from qrcode.views import index, aprovado, negado, validar, gerador, validador, cadastro, validado, checkin, buscar_email_por_cnpj, cadastrar_password, cadastrar_senha

urlpatterns = [
    path('', index, name="index"),
    path('validar/', validar, name='validar'),
    path("aprovado", aprovado, name="aprovado"),
    path("negado", negado, name="negado"),
    path("validado", validado, name="validado"),
    path("gerador/", gerador, name="gerador"),
    path('validador/', validador, name="validador"),
    path('cadastro/', cadastro, name="cadastro"),
    path('checkin/', checkin, name="checkin"),
    path('buscar-email/', buscar_email_por_cnpj,
         name='buscar_email_por_cnpj'),
    path('cadastrar-senha/', cadastrar_password, name='cadastrar_password'),
    path('cadastrar-senha/confirmar/', cadastrar_senha, name='cadastrar_senha')
]
