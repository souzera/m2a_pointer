from django.db import models

from .utils import getTimeDiff

class Empresa(models.Model):

    '''
    [PT]

        Informações sobre uma empresa

        nome: Nome da empresa
        endereco: Endereço da empresa

    [EN]

        Information about a company

        nome: Company name
        endereco: Company address
    
    '''
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=256)

    def __str__(self):
        return self.nome

class Funcionario(models.Model):

    '''
    [PT]

        Informações sobre um funcionário

        usuario: Usuário ao qual o funcionário pertence
        nome: Nome do funcionário
        email: Email do funcionário
        empresa: Empresa a qual o funcionário pertence

    [EN]

        Information about an employee

        usuario: User to which the employee belongs
        nome: Employee name
        email: Employee email
        empresa: Company to which the employee belongs

    '''

    usuario = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nome} - {self.empresa.nome}"

class Ponto(models.Model):
    '''
    [PT]

        Informações sobre o ponto de um funcionário

        funcionario: Funcionário ao qual o ponto pertence
        data: Dia em qual foi realizado o registro do ponto
        entrada: Horário de entrada
        saida: Horário de saída

        o atributos `entrada` e `saida` tem os valores setados automaticamente para o horário o qual o usuario dispara uma ação na aplicação

    [EN]

        Information about an employee's point

        funcionario: Employee to which the point belongs
        data: Day on which the point was registered
        entrada: Entry time
        saida: Exit time

        the `entrada` and `saida` attributes have their values set automatically to the time at which the user triggers an action in the application
    '''
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
        return f"{self.funcionario.nome} - {self.data}"
