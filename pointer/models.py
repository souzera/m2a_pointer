from django.db import models

from .utils import getTimeDiff

class Empresa(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=256)

    def __str__(self):
        return self.nome

class Funcionario(models.Model):
    usuario = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nome} - {self.empresa.nome}"

class Ponto(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    data = models.DateField(auto_created=True)
    entrada = models.TimeField(auto_created=True, auto_now_add=True)
    saida = models.TimeField(blank=True, null=True)

    def get_diff(self):
        '''
        [PT]
            @return (float): A diferença de tempo entre a entrada e a saída em horas

        [EN]
            @return (float): The time difference between the entry and exit in hours
        '''
        from datetime import datetime
        return getTimeDiff(datetime.combine(self.data, self.entrada), datetime.combine(self.data, self.saida))/3600

    def __str__(self):
        diff = ''
        try:
            diff = self.get_diff()
        except:
            pass
        return f"{self.funcionario.nome} - {self.data}"
