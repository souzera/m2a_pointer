from django.contrib.auth.views import *
from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
    path('register/', RegisterPageView.as_view(), name='register'),
    path('login/', LoginPageView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', DashboardPageView.as_view(), name='dashboard'),
    path('empresa/register/', RegisterEmpresaPageView.as_view(), name='register_empresa'),
    path('record_point/', record_point, name='record_point'),
]