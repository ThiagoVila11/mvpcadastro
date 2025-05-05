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
    path('documentos/<int:cliente_id>/', views.visualizar_documento, name='visualizar_documento'),
    #condominio
    path('cadastro_condominio/', views.cadastro_condominio, name='cadastro_condominio'),
    path('get_dados_condominio/', views.get_dados_condominio, name='get_dados_condominio'),
    path('get_condominio_completo/', views.get_condominio_completo, name='get_condominio_completo'),
    #apartamento
    path('cadastro_apartamento/', views.cadastro_apartamento, name='cadastro_apartamento'),  
    path('get_apartamentos/', views.get_apartamentos, name='get_apartamentos'), 
]
