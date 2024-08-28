from django.urls import path
from . import views

urlpatterns = [
    path('<str:page>/', views.render_page, name='render_page'),
    path('', views.render_page, {'page': 'index'}, name='home'),
    path('process_form/', views.process_form, name='process_form'),
]
