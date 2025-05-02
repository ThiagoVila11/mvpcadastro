from django.urls import path
from . import views

urlpatterns = [
    path('', views.cadastro_cliente, name='cadastro'),
    path('cadastro_cliente/', views.cadastro_cliente, name='cadastro_cliente'),
    path('sucesso/', views.sucesso, name='sucesso'),
    path('clientes/consulta/', views.consulta_clientes, name='consulta_clientes'),
    path('clientes/<int:id>/detalhes/', views.detalhes_cliente, name='detalhes_cliente'),
    path('clientes/<int:id>/editar/', views.editar_cliente, name='editar_cliente'),
    path('consulta/', views.consulta_view, name='consulta'),
    path('consulta-cpf/', views.consulta_cpf, name='consulta_cpf'),
    path('preencher_pdf/<int:cliente_id>/', views.preencher_pdf, name='preencher_pdf'),
    path('outro-pdf/', views.outro_pdf, name='outro_pdf'),
]
