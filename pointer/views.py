from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth import authenticate

from django.http import HttpResponse

class HomePageView(TemplateView):
    template_name = 'index.html'

class RegisterPageView(TemplateView):
    template_name = 'register.html'

    def validate_form(self, form):
        print(form)
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
        data = request.POST.dict()
        errors = self.validate_form(data)

        if len(errors) != 0:
            return render(request, self.template_name, {'errors': errors})
        
        # Create user
        
        return HttpResponse('Usuário cadastrado com sucesso')
    

class LoginPageView(TemplateView):
    template_name = 'login.html'

    def post(self, request):
        data = request.POST.dict()
        
        print(data)

        user = authenticate(username=data['username'], password=data['password'])
        print(user)
        # Login user

        return HttpResponse('Usuário logado com sucesso')