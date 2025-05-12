from django.urls import path
from . import views
from cadastro.views import CondominioKPIDashboard


urlpatterns = [
    path('', CondominioKPIDashboard.as_view(), name='cadastro'),
    path('cadastro_cliente/', views.cadastro_cliente, name='cadastro_cliente'),
    path('sucesso/', views.sucesso, name='sucesso'),
    path('clientes/consulta/', views.consulta_clientes, name='consulta_clientes'),
    path('clientes/<int:id>/detalhes/', views.detalhes_cliente, name='detalhes_cliente'),
    path('clientes/<int:id>/editar/', views.editar_cliente, name='editar_cliente'),
    path('clientes/excluir/<int:id>/', views.excluir_cliente, name='excluir_cliente'),
    path('consulta/', views.consulta_view, name='consulta'),
    path('consulta-cpf/', views.consulta_cpf, name='consulta_cpf'),
    path('preencher_pdf/<int:cliente_id>/', views.preencher_pdf, name='preencher_pdf'),
    path('documentos/<int:cliente_id>/', views.visualizar_documento, name='visualizar_documento'),
    #condominio
    path('cadastro_condominio/', views.cadastro_condominio, name='cadastro_condominio'),
    path('consulta_condominios/', views.consulta_condominios, name='consulta_condominios'),
    path('condominio/<int:id>/detalhes/', views.detalhes_condominio, name='detalhes_condominio'),
    path('condominio/<int:id>/editar/', views.editar_condominio, name='editar_condominio'),
    path('condominio/excluir/<int:id>/', views.excluir_condominio, name='excluir_condominio'),
    path('get_dados_condominio/', views.get_dados_condominio, name='get_dados_condominio'),
    path('get_condominio_completo/', views.get_condominio_completo, name='get_condominio_completo'),
    #apartamento
    path('cadastro_apartamento/', views.cadastro_apartamento, name='cadastro_apartamento'),  
    path('consulta_apartamentos/', views.consulta_apartamentos, name='consulta_apartamentos'),
    path('apartamento/<int:id>/detalhes/', views.detalhes_apartamento, name='detalhes_apartamento'),
    path('apartamento/<int:id>/editar/', views.editar_apartamento, name='editar_apartamento'),
    path('apartamento/excluir/<int:id>/', views.excluir_apartamento, name='excluir_apartamento'),
    path('get_apartamentos/', views.get_apartamentos, name='get_apartamentos'), 
    #consultores
    path('cadastro_consultor/', views.cadastro_consultor, name='cadastro_consultor'),
    path('consulta_consultores/', views.consulta_consultores, name='consulta_consultores'),

    
    #pré-cliente
    path('cadastro_precliente/', views.cadastro_precliente, name='cadastro_precliente'),
    path('consulta_preclientes', views.consulta_preclientes, name='consulta_preclientes'),
    path('precliente/<int:id>/detalhes/', views.detalhes_precliente, name='detalhes_precliente'),
    path('precliente/<int:id>/editar/', views.editar_precliente, name='editar_precliente'),
    path('precliente/converter/<int:precliente_id>/', views.converter_precliente, name='converter_precliente'),
    path('precliente/excluir/<int:id>/', views.excluir_precliente, name='excluir_precliente'),
    #dashboards
    path('condominios/kpi/', CondominioKPIDashboard.as_view(), name='kpi-condominios')

]
