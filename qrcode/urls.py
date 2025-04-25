from django.urls import path
from qrcode.views import index, aprovado, negado, validar, gerador, validador, cadastro, validado, gerar_pdf_qrcodes, checkin

urlpatterns = [
    path('', index, name="index"),
    path('validar/', validar, name='validar'),
    path("aprovado", aprovado, name="aprovado"),
    path("negado", negado, name="negado"),
    path("validado", validado, name="validado"),
    path("gerador/", gerador, name="gerador"),
    path('gerar_pdf_qrcodes/', gerar_pdf_qrcodes, name='gerar_pdf_qrcodes'),
    # path("gerador2/", gerador2, name="gerador2"),
    path('validador/', validador, name="validador"),
    path('cadastro/', cadastro, name="cadastro"),
    path('checkin/', checkin, name="checkin"),

]
