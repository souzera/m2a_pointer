from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.models import User
from .models import *

from django.http import HttpResponse

class HomePageView(TemplateView):
    template_name = 'index.html'

class RegisterPageView(TemplateView):
    template_name = 'register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['empresas'] = Empresa.objects.all().order_by('nome')
        context['errors'] = []
        
        return context

    def validate_form(self, form):
        '''
        [PT]
            @param form: dicionário com os dados do formulário

            @return: lista de nomes de erros encontrados: list(strings)

        [EN]

            @param form: dictionary with form data

            @return: list of error names found: list(strings)

        '''

        errors = []
        if len(form['username']) < 3 or len(form['username']) > 16:
            errors.append('INVALID_USER')
        if len(form['password']) < 8:
            errors.append('INVALID_PASSWORD')
        if form['password'] != form['confirm-password']:
            errors.append('UNEQUAL_PASSWORD')
        from django.contrib.auth.models import User
        if User.objects.filter(username=form['username']).exists():
            errors.append('USER_UNAVAILABLE')

        return errors

    def post(self, request):
        '''
        [PT]

        Etepas:
        1. Pegar os dados do formulário
        2. Validar os dados
        3. Criação o usuário
        4. Redirecionar para o dashboard ou renderizar a página de registro com os erros

        nt.: O usuario deve solicitar o acesso ao time da empresa apos o cadastro do usuario

        @param request: HttpRequest
        @return: redirencionar para o dashboard ou renderizar a página de registro com os erros

        [EN]

        Steps:
        1. Get form data
        2. Validate data
        3. Create user
        4. Redirect to dashboard or render register page with errors

        Note: The user must request access to the company's team after registering the user

        @param request: HttpRequest
        @return: redirect to dashboard or render register page with errors

        '''
        data = request.POST.dict()
        errors = self.validate_form(data)

        if len(errors) != 0:
            return render(request, self.template_name, {'errors': errors})
        
        # Create user
        user = User.objects.create_user(data['username'], data['email'], data['password'])

        user.first_name = data['name'].split(' ')[0]
        user.last_name = data['name'].split(' ')[1] if len(data['name'].split(' ')) > 1 else ''
        user.save()

        # Create funcionario

        empresa = Empresa.objects.get(id=data['empresa'])
        funcionario = Funcionario.objects.create(usuario=user, nome=data['name'], email=data['email'], empresa=empresa)

        # Autenticar o usuário

        user = authenticate(username=data['username'], password=data['password'])
        login(request, user)

        return redirect('dashboard')

class LoginPageView(TemplateView):
    template_name = 'login.html'

    def post(self, request):
        data = request.POST.dict()

        user = authenticate(username=data['username'], password=data['password'])

        # Login user
        if user is not None:
            login(request, user)
            return redirect('dashboard')

        return render(request, self.template_name, {'errors': ['INVALID_DATA']})

def logout_view(request):
    logout(request)
    return redirect('login')

class DashboardPageView(LoginRequiredMixin,TemplateView):
    template_name = 'dashboard.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        
        funcionario = Funcionario.objects.get(usuario=context['user'])
        empresa = Empresa.objects.get(id=funcionario.empresa.id)
        pontos = Ponto.objects.filter(funcionario=funcionario).order_by('-data')

        context['funcionario'] = funcionario
        context['empresa'] = empresa
        context['pontos'] = pontos

        return context