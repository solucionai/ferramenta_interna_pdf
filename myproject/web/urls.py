from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Mapeia a URL raiz para a view 'home'
]

