from django.core.management.base import BaseCommand
# substitua 'core' pelo nome real do seu app
from qrcode.models import ClienteQtd


class Command(BaseCommand):
    help = 'Popula a tabela ClienteQtd com dados fictícios para testes'

    def handle(self, *args, **kwargs):
        dados_ficticios = [
            {
                'cnpj': '11222333000181',
                'razsoc': 'Agro Alfa LTDA',
                'email': 'contato@agroalfa.com.br',
                'qtd_convites': 2
            },
            {
                'cnpj': '44556677000192',
                'razsoc': 'Fazenda Boa Terra LTDA',
                'email': 'boaterra@fazendas.com.br',
                'qtd_convites': 2
            },
            {
                'cnpj': '99887766000104',
                'razsoc': 'Campo Forte Agro',
                'email': 'contato@campoforte.com.br',
                'qtd_convites': 2
            },
            {
                'cnpj': '12345678000155',
                'razsoc': 'Rural Primeira Semente',
                'email': 'rps@ruralprimeira.com.br',
                'qtd_convites': 2
            },
            {
                'cnpj': '55443322000167',
                'razsoc': 'Sementes do Vale Ltda',
                'email': 'svl@sementesvale.com.br',
                'qtd_convites': 2
            }
        ]

        for item in dados_ficticios:
            cliente, criado = ClienteQtd.objects.get_or_create(
                cnpj=item['cnpj'],
                defaults={
                    'razsoc': item['razsoc'],
                    'email': item['email'],
                    'qtd_convites': item['qtd_convites'],
                }
            )
            if criado:
                self.stdout.write(self.style.SUCCESS(f'Inserido: {cliente}'))
            else:
                self.stdout.write(self.style.WARNING(f'Já existe: {cliente}'))
