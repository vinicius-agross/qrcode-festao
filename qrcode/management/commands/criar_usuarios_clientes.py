from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from qrcode.models import ClienteQtd


class Command(BaseCommand):
    help = 'Cria usuários Django a partir da tabela ClienteQtd com senha padrão baseada em CNPJ e email'

    def handle(self, *args, **kwargs):
        clientes = ClienteQtd.objects.all()
        for cliente in clientes:
            if not cliente.email or not cliente.cnpj:
                self.stdout.write(self.style.WARNING(
                    f'Skipping: {cliente} (sem email ou CNPJ)'))
                continue

            username = cliente.cnpj
            email = cliente.email
            email_prefix = email.split('@')[0]
            senha_padrao = f'{username[:4]}@{email_prefix}'

            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=senha_padrao
                )
                user.first_name = cliente.razsoc or ""
                user.save()

                self.stdout.write(self.style.SUCCESS(
                    f'Usuário criado: {username} | senha: {senha_padrao}'
                ))
            else:
                self.stdout.write(f'Usuário já existe: {username}')
