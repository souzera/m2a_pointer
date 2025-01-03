from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from .models import *

from django.http import HttpResponse,  JsonResponse

from datetime import datetime
import json


class HomePageView(TemplateView):
    '''
    [PT]
        Página inicial

    [EN]
        Home page
    '''
    template_name = 'index.html'

class RegisterPageView(TemplateView):
    '''
    [PT]
        Página de registro

    [EN]
        Register page

    '''
    template_name = 'register.html'

    def get_context_data(self, **kwargs):
        '''
        [PT]

            Adicionar informações ao contexto

            @param kwargs: dict
            @return: dict
        
        [EN]

            Add information to the context

            @param kwargs: dict
            @return: dict
        '''

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

        context = self.get_context_data()

        if len(errors) != 0:
            context['errors'] = errors
            return render(request, self.template_name, context)
        
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
    '''
    [PT]
        Página de login
    
    [EN]
        Login page
    '''
    template_name = 'login.html'

    def post(self, request):
        '''
        [PT]

            Realiza a autenticação do usuário
            Consulta o banco de dados para verificar se o usuário existe
            Se o usuário existir, redireciona para o dashboard

            @param request: HttpRequest
            @return: redirecionar para o dashboard ou renderizar a página de login com os erros

        [EN]

            Authenticate the user
            Query the database to check if the user exists
            If the user exists, redirect to the dashboard

            @param request: HttpRequest
            @return: redirect to dashboard or render login page with errors
        '''
        data = request.POST.dict()

        user = authenticate(username=data['username'], password=data['password'])

        # Login user
        if user is not None:
            login(request, user)
            return redirect('dashboard')

        return render(request, self.template_name, {'errors': ['INVALID_DATA']})

def logout_view(request):
    '''
    [PT]
        Remover a sessão do usuário

        @param request: HttpRequest
        @return: redirecionar para a página de login

    [EN]
        Remove the user's session

        @param request: HttpRequest
        @return: redirect to login page
    '''
    logout(request)
    return redirect('login')

class DashboardPageView(LoginRequiredMixin,TemplateView):
    '''
    [PT]

        Página de dashboard
        Mostra todos os pontos do funcionario
        Também possibilita os registros dos pontos

        LoginRequiredMixin: Verifica se o usuário está logado

    [EN]

        Dashboard page
        Shows all employee's points
        Also allows point registration

        LoginRequiredMixin: Check if the user is logged in
    '''
    template_name = 'dashboard.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        '''
        [PT]

            Adicionar informações ao contexto

            @param kwargs: dict
            @return: dict
        
        [EN]

            Add information to the context

            @param kwargs: dict
            @return: dict
        '''
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        
        funcionario = Funcionario.objects.get(usuario=context['user'])
        empresa = Empresa.objects.get(id=funcionario.empresa.id)
        pontos = Ponto.objects.filter(funcionario=funcionario).order_by('-data')

        context['funcionario'] = funcionario
        context['empresa'] = empresa
        context['pontos'] = pontos

        return context
    

class RegisterEmpresaPageView(TemplateView):
    '''
    [PT]

        Página de registro de empresa

    [EN]

        Register company page
    '''
    template_name = 'empresa/register.html'

    def post(self, request):
        '''
        [PT]

            Cadastrar empresa

            @param request: HttpRequest
            @return: renderizar a página de registro com a mensagem de sucesso ou erro

        [EN]

            Register company

            @param request: HttpRequest
            @return: render register page with success or error message
        '''
        data = request.POST.dict()
        print(data)

        try:
            empresa = Empresa.objects.create(nome=data['name'], endereco=data['address'])
            return render(request, self.template_name, {'success': f"{empresa.nome} cadastrada com sucesso!"})
        except:
            return render(request, self.template_name, {'error': f"Erro ao cadastrar {data['name']}"})


@login_required(login_url='/login/')
def record_point(request):

    '''
    [PT]

        Registrar ponto do funcionario
        A função verifica se o ponto do funcionario já foi registrado no dia, caso sim, registra a saída
        Caso contrário, registra a entrada.
         
        A atualização é renderizada na página do diário e no dashboard

        @param request: HttpRequest
        @return: JsonResponse

    [EN]

        Register employee's point
        The function checks if the employee's point has already been registered on the day, if so, it registers the exit
        Otherwise, it registers the entry.

        The update is rendered on the diary page and on the dashboard

        @param request: HttpRequest
        @return: JsonResponse
    '''

    data = json.loads(request.body.decode('utf-8'))

    day = datetime.strptime(data['data'], "%Y-%m-%dT%H:%M:%S.%fZ")
    ponto = Ponto.objects.filter(data__year=day.year, data__month=day.month, data__day=day.day, funcionario__usuario=request.user).first()

    if ponto and ponto.saida:
        return JsonResponse({
            "functionario": ponto.funcionario.nome,
            "message": "Ponto já registrado",
            "data": ponto.data.strftime('%Y-%m-%d'),
            'status': 'error'
        })

    if ponto:
        # Horario de saída
        agora = datetime.now().time()
        ponto.saida = agora
        ponto.save()
        return JsonResponse({
            "functionario": ponto.funcionario.nome,
            "data": ponto.data.strftime('%Y-%m-%d'),
            'entrada': ponto.entrada.strftime('%H:%M:%S'),
            'saida': ponto.saida.strftime('%H:%M:%S'),
            'status': 'success',
            "message": "Saída registrada com sucesso"
        })

    # Horario de entrada
    ponto = Ponto.objects.create(data=day, funcionario=Funcionario.objects.get(usuario=request.user))
    return JsonResponse({
        "functionario": ponto.funcionario.nome,
        "data": ponto.data.strftime('%Y-%m-%d'),
        'entrada': ponto.entrada.strftime('%H:%M:%S'),
        'status': 'success',
        'message': "Entrada registrada com sucesso"
    })


class DiarioPageView(LoginRequiredMixin, TemplateView):
    '''
    [PT]

        Página de diário
        Lista os pontos de todos os funcionários da empresa
        Filtragem dos pontos por data
        Data inicial: data atual

        LoginRequiredMixin: Verifica se o usuário está logado

    [EN]

        Diary page
        Lists the points of all employees in the company
        Filtering points by date
        Initial date: current date

        LoginRequiredMixin: Check if the user is logged in
    '''

    template_name = 'empresa/diario.html'
    login_url = '/login/'

    def post(self, request):
        '''
        [PT]
            Filtrar os pontos do funcionario por data

            @param request: HttpRequest
            @return: renderizar a página de diário com os pontos filtrados
        [EN]

            Filter the employee's points by date

            @param request: HttpRequest
            @return: render the diary page with the filtered points
        '''

        data = request.POST.dict()
        selected_date = datetime.strptime(data['date'], "%Y-%m-%d")
        
        context = self.get_context_data()

        context['date'] = selected_date.strftime('%Y-%m-%d')
        context['pontos'] = Ponto.objects.filter(funcionario__empresa=context['empresa'], data=context['date'])

        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        '''
        [PT]

            Adicionar informações ao contexto

            @param kwargs: dict
            @return: dict
        
        [EN]

            Add information to the context

            @param kwargs: dict
            @return: dict
        '''
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['date'] = datetime.now().strftime('%Y-%m-%d')
        
        funcionario = Funcionario.objects.get(usuario=context['user'])
        empresa = Empresa.objects.get(id=funcionario.empresa.id)
        pontos = Ponto.objects.filter(funcionario__empresa=empresa, data=context['date'])

        context['funcionario'] = funcionario
        context['empresa'] = empresa
        context['pontos'] = pontos

        return context