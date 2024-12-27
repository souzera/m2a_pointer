from django.db import models

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
    entrada = models.TimeField()
    saida = models.TimeField()

    def __str__(self):
        return f"{self.funcionario.nome} - {self.data}"
