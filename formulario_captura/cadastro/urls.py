from django.urls import path
from . import views

urlpatterns = [
    path('', views.cadastro_cliente, name='cadastro'),
    path('sucesso/', views.sucesso, name='sucesso'),
    path('clientes/consulta/', views.consulta_clientes, name='consulta_clientes'),
    path('clientes/<int:id>/detalhes/', views.detalhes_cliente, name='detalhes_cliente'),
    path('clientes/<int:id>/editar/', views.editar_cliente, name='editar_cliente'),
]