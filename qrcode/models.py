from django.db import models


class Cliente(models.Model):
    cpf = models.CharField(max_length=11, primary_key=True)
    cnpj = models.CharField(max_length=14)
    razsoc = models.CharField(max_length=100, null=True, blank=True)
    nome = models.CharField(max_length=100, null=True, blank=True)
    checkin = models.CharField(max_length=1, null=True, blank=True)
    data_hora = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'CLIENTE_CONVIDADO'
        managed = True  # Alterado para True para que o Django gerencie a tabela

    def __str__(self):
        return f'{self.nome} ({self.cpf})'


class ClienteQtd(models.Model):
    cnpj = models.CharField(max_length=14, primary_key=True)
    razsoc = models.CharField(max_length=100, null=True, blank=True)
    qtd_convites = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'CLIENTE'
        managed = True  # Alterado para True para que o Django gerencie a tabela

    def __str__(self):
        return f'{self.cnpj} - {self.qtd_convites} convites'
