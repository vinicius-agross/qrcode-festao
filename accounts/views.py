from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from qrcode.models import ClienteQtd
from django.utils.http import urlencode


def cadastro_senha(request):
    cnpj = request.GET.get('cnpj')

    if not cnpj:
        messages.error(request, "CNPJ inválido ou não fornecido.")
        return redirect('register')

    try:
        cliente = ClienteQtd.objects.get(cnpj=cnpj)
        # Ajuste para o campo de e-mail correto
        email = f"{cliente.razsoc}@example.com"

        if request.method == 'POST':
            senha = request.POST.get('password1')
            senha_confirmacao = request.POST.get('password2')

            if not senha or not senha_confirmacao:
                messages.error(
                    request, "Por favor, preencha os dois campos de senha.")
                return render(request, 'cadastro/cadastro_senha.html', {'cnpj': cnpj})

            if senha != senha_confirmacao:
                messages.error(request, "As senhas não coincidem.")
                return render(request, 'cadastro/cadastro_senha.html', {'cnpj': cnpj})

            # Cria o usuário
            user = User.objects.create(
                username=cnpj,
                email=email,
                password=make_password(senha)
            )

            messages.success(
                request, "Cadastro realizado com sucesso! Você já pode fazer login.")
            return redirect('login')

        return render(request, 'cadastro/cadastro_senha.html', {'cnpj': cnpj})

    except ClienteQtd.DoesNotExist:
        messages.error(request, "CNPJ não encontrado.")
        return redirect('register')
