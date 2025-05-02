from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from qrcode.models import ClienteQtd
from django.db import transaction


class Command(BaseCommand):
    help = 'Cria usuários Django a partir da tabela ClienteQtd com senha padrão baseada em CNPJ e email'

    def handle(self, *args, **kwargs):
        # Buscar apenas os campos necessários
        clientes = ClienteQtd.objects.only(
            'cnpj', 'razsoc', 'email', 'qtd_convites')

        # Buscar usernames existentes em uma única consulta
        usernames_existentes = set(
            User.objects.values_list('username', flat=True))

        novos_users = []

        with transaction.atomic():  # Evita múltiplos commits desnecessários
            for cliente in clientes:
                if not cliente.email or not cliente.cnpj:
                    self.stdout.write(self.style.WARNING(
                        f'Skipping: {cliente} (sem email ou CNPJ)'))
                    continue

                username = cliente.cnpj

                if username in usernames_existentes:
                    self.stdout.write(f'Usuário já existe: {username}')
                    continue

                email = cliente.email
                email_prefix = email.split('@')[0]
                senha_padrao = f'{username[:4]}@{email_prefix}'

                # Criação em memória (bulk create depois)
                user = User(
                    username=username,
                    email=email,
                    first_name=cliente.razsoc or ""
                )
                user.set_password(senha_padrao)
                novos_users.append(user)

        # Inserir em lote (melhor performance)
        if novos_users:
            User.objects.bulk_create(novos_users)
            self.stdout.write(self.style.SUCCESS(
                f'{len(novos_users)} usuários criados com sucesso.'
            ))
