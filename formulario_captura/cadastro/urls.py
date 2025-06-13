from django.urls import path
from . import views
from . import api
from cadastro.views import CondominioKPIDashboard
from .api import get_consultor_id_by_email
from django.conf.urls.static import static
from django.conf import settings
from .views import ClienteListView, NotificacaoListView



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
    path('assinar_contrato/<int:cliente_id>/', views.assinar_contrato, name='assinar_contrato'),
    path('documentos/<int:cliente_id>/', views.visualizar_documento, name='visualizar_documento'),
    path('webhook/', views.webhook_receiver, name='webhook_receiver'),
    path('finalizar_atendimento/<int:cliente_id>/', views.finalizar_atendimento, name='finalizar_atendimento'),
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
    path('consultor/excluir/<int:id>/', views.excluir_consultor, name='excluir_consultor'),
    path('consultor/<int:id>/editar/', views.editar_consultor, name='editar_consultor'),
    path('consultor/<int:id>/detalhes/', views.detalhes_consultor, name='detalhes_consultor'),    
    #pré-cliente
    path('cadastro_precliente/', views.cadastro_precliente, name='cadastro_precliente'),
    path('consulta_preclientes', views.consulta_preclientes, name='consulta_preclientes'),
    path('precliente/<int:id>/detalhes/', views.detalhes_precliente, name='detalhes_precliente'),
    path('precliente/<int:id>/editar/', views.editar_precliente, name='editar_precliente'),
    path('precliente/converter/<int:precliente_id>/', views.converter_precliente, name='converter_precliente'),
    path('precliente/excluir/<int:id>/', views.excluir_precliente, name='excluir_precliente'),
    #dashboards
    path('condominios/kpi/', CondominioKPIDashboard.as_view(), name='kpi-condominios'),
    #API´s
    path('api/consultor/', get_consultor_id_by_email, name='get_consultor_id_by_email'),
    path('api/clientes/', ClienteListView.as_view(), name='lista-clientes'),
    path('api/notificacoes/', NotificacaoListView.as_view(), name='notificacoes-list'),
    # notificações
    path('notificacoes/', views.notificacoes_view, name='notificacoes'),
    path('ajax/notificacoes/', views.notificacoes_ajax, name='notificacoes_ajax'),
    path('ajax/marcar_lida/', views.marcar_notificacao_lida, name='marcar_notificacao_lida'),

]+ static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])