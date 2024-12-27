from django.contrib.auth.views import *
from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
]