from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .forms import ClienteForm, CondominioForm, ApartamentoForm, ConsultorForm, PreClienteForm
from .models import Cliente, Condominio, Apartamento, Consultor, PreCliente, Notificacao, LogAcesso
from django.db.models import Q, Count
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseNotAllowed
from .services.api_service import APIDataBuscaService
import json
from django.template.loader import render_to_string
from docxtpl import DocxTemplate
import pdfkit
from PyPDF2 import PdfReader, PdfWriter
import os
from django.conf import settings 
from django.http import HttpResponse, FileResponse, Http404
import re
from datetime import datetime
from io import BytesIO
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
import requests
from django.contrib.auth import get_user_model
import logging
from requests.exceptions import RequestException
from django.db.models import Count, Sum, Avg
from plotly.offline import plot
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
from functools import wraps
from django.http import HttpResponseForbidden
from django.views.generic import TemplateView
from .serializers import ConsultorSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response  # Este import é crucial
from django.views.decorators.http import require_http_methods
from decimal import Decimal
from django.core.files.base import ContentFile
from .serializers import ClienteSerializer, NotificacaoSerializer, ClienteCrudSerializer
from rest_framework import generics, viewsets


def requer_consultor(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.session.get('api_funcao') == 'CONSULTOR':
            return render(request, 'erros/sem_permissao.html', status=403)
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def valida_consultor(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Adiciona uma variável ao contexto indicando se é consultor
        is_consultor = request.session.get('api_funcao') == 'CONSULTOR'
            
        response = view_func(request, *args, **kwargs)
        
        # Se for uma TemplateResponse ou HttpResponse, adiciona o contexto
        if hasattr(response, 'context_data'):
            response.context_data['is_consultor'] = is_consultor
        elif isinstance(response, render):
            response.context_data = response.context_data or {}
            response.context_data['is_consultor'] = is_consultor
        #print(response)    
        return response
    return _wrapped_view

@login_required(login_url='/login/')
def cadastro_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES)
        #print(form)
        if form.is_valid():
            form.save()
            return redirect('sucesso')
    else:
        form = ClienteForm()
    
    return render(request, 'cadastro/formulario.html', {'form': form})

def sucesso(request):
    return render(request, 'cadastro/sucesso.html')

@login_required(login_url='/login/') 
def consulta_clientes(request):
    nome = request.GET.get('nome', '')
    cpf = request.GET.get('cpf', '')
    finalizado = request.GET.get('finalizado', '')

    clientes = Cliente.objects.all()

    if nome:
        clientes = clientes.filter(nome__icontains=nome)

    if cpf:
        clientes = clientes.filter(cpf__icontains=cpf)

    if finalizado == '1':
        clientes = clientes.filter(processofinalizado=True)
    elif finalizado == '0':
        clientes = clientes.filter(processofinalizado=False)

    context = {
        'clientes': clientes,
        'filtros': {
            'nome': nome,
            'cpf': cpf,
            'finalizado': finalizado,
        },
        'is_consultor': request.user.groups.filter(name='Consultores').exists()
    }
    return render(request, 'consulta_clientes.html', context)


@login_required(login_url='/login/') 
def detalhes_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    return render(request, 'detalhes_cliente.html', {'cliente': cliente})

@login_required(login_url='/login/') 
def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    condominios = Condominio.objects.all()
    apartamentos = Apartamento.objects.filter(Condominio=cliente.Condominio) if cliente.Condominio else Apartamento.objects.none()

    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES, instance=cliente)
        if form.is_valid():
            # Processar campos especiais antes de salvar
            instance = form.save(commit=False)
            
            # Atualizar condomínio e apartamento
            condominio_id = request.POST.get('Condominio')
            apartamento_id = request.POST.get('Apartamento')
            
            if condominio_id:
                instance.Condominio = Condominio.objects.get(id=condominio_id)
            if apartamento_id:
                instance.Apartamento = Apartamento.objects.get(id=apartamento_id)
            
            instance.save()
            return redirect('detalhes_cliente', id=instance.id)
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'editar_cliente.html', {
        'cliente': cliente,
        'form': form,
        'condominios': condominios,
        'apartamentos': apartamentos,
        'is_consultor': request.session.get('api_funcao') == 'CONSULTOR'
    })

@login_required(login_url='/login/') 
def excluir_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    
    if request.method == 'POST':
        try:
            cliente.delete()
            messages.success(request, 'Cliente excluído com sucesso!')
            return redirect('consulta_clientes')
        except Exception as e:
            messages.error(request, f'Erro ao excluir cliente: {str(e)}')
            return redirect('detalhes_cliente', id=id)
    
    # Se não for POST, mostra página de confirmação
    return render(request, 'confirmar_exclusao.html', {'cliente': cliente})

@csrf_exempt
def finalizar_atendimento(request, cliente_id):
    if request.method == "POST":
        observacao = request.POST.get('observacao')
        try:
            cliente = Cliente.objects.get(id=cliente_id)
            cliente.visitarealizada = True  
            cliente.processofinalizado = True  
            cliente.observacoes = observacao
            cliente.save()
            return JsonResponse({'success': True})
        except Cliente.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Cliente não encontrado'})
    return JsonResponse({'success': False, 'error': 'Requisição inválida'})

@login_required(login_url='/login/') 
@requer_consultor
def cadastro_condominio(request):
    if request.method == 'POST':
        form = CondominioForm(request.POST, request.FILES)
        #print(form)
        if form.is_valid():
            form.save()
            return redirect('sucesso')
    else:
        form = CondominioForm()
    
    return render(request, 'cadastro/formulariocondominio.html', {'form': form})

@login_required(login_url='/login/') 
def consulta_condominios(request):
    # Obtém todos os clientes inicialmente
    condominios = Condominio.objects.all().order_by('condominionome')
    #print(condominios)
    
    # Filtros
    nome = request.GET.get('nome')
    #print('Nome:')
    #print(nome)
    if nome:
        condominios = condominios.filter(Q(condominionome__icontains=nome))
    
    context = {
        'condominios': condominios,
        'filtros': {
            'condominionome': nome or ''
        }
    }
    #print(context)
    return render(request, 'consulta_condominios.html', context)

@login_required(login_url='/login/') 
@requer_consultor
def detalhes_condominio(request, id):
    condominio = get_object_or_404(Condominio, id=id)
    return render(request, 'detalhes_condominio.html', {'condominio': condominio})

@login_required(login_url='/login/') 
@requer_consultor
def editar_condominio(request, id):
    condominio = get_object_or_404(Condominio, id=id)
    
    if request.method == 'POST':
        form = CondominioForm(request.POST, request.FILES, instance=condominio)
        if form.is_valid():
            form.save()
            return redirect('detalhes_condominio', id=condominio.id)
    else:
        form = CondominioForm(instance=condominio)
    
    return render(request, 'editar_condominio.html', {
        'form': form,
        'condominio': condominio
    })

@login_required(login_url='/login/') 
@requer_consultor
def excluir_condominio(request, id):
    condominio = get_object_or_404(Condominio, id=id)
    
    if request.method == 'POST':
        try:
            condominio.delete()
            messages.success(request, 'Condominio excluído com sucesso!')
            return redirect('consulta_condominios')
        except Exception as e:
            messages.error(request, f'Erro ao excluir condominio: {str(e)}')
            return redirect('detalhes_condominio', id=id)
    
    # Se não for POST, mostra página de confirmação
    return render(request, 'confirmarexclusaocondominio.html', {'condominio': condominio})

@login_required(login_url='/login/') 
@requer_consultor
def cadastro_apartamento(request):
    if request.method == 'POST':
        form = ApartamentoForm(request.POST, request.FILES)
        #print(form)
        if form.is_valid():
            form.save()
            return redirect('sucesso')
    else:
        form = ApartamentoForm()
    
    return render(request, 'cadastro/formularioapartamento.html', {'form': form})

@login_required(login_url='/login/') 
def consulta_apartamentos(request):
    apartamentos = Apartamento.objects.all().order_by('apartamentonro')
    
    # Filtros
    nome = request.GET.get('nome')
    if nome:
        apartamentos = apartamentos.filter(Q(apartamentonro__icontains=nome))
    
    context = {
        'apartamentos': apartamentos,
        'filtros': {
            'apartamentonro': nome or ''
        }
    }
    #print(context)
    return render(request, 'consulta_apartamentos.html', context)

@login_required(login_url='/login/') 
@requer_consultor
def editar_apartamento(request, id):
    apartamento = get_object_or_404(Apartamento, id=id)
    
    if request.method == 'POST':
        form = ApartamentoForm(request.POST, request.FILES, instance=apartamento)
        if form.is_valid():
            form.save()
            return redirect('detalhes_apartamento', id=apartamento.id)
    else:
        form = ApartamentoForm(instance=apartamento)
    
    return render(request, 'editar_apartamento.html', {
        'form': form,
        'apartamento': apartamento
    })

@login_required(login_url='/login/')
@requer_consultor
def detalhes_apartamento(request, id):
    apartamento = get_object_or_404(Apartamento, id=id)
    return render(request, 'detalhes_apartamento.html', {'apartamento': apartamento})

@login_required(login_url='/login/') 
@requer_consultor
def excluir_apartamento(request, id):
    apartamento = get_object_or_404(Apartamento, id=id)
    
    if request.method == 'POST':
        try:
            apartamento.delete()
            messages.success(request, 'Apartamento excluído com sucesso!')
            return redirect('consulta_apartamentos')
        except Exception as e:
            messages.error(request, f'Erro ao excluir apartamento: {str(e)}')
            return redirect('detalhes_apartamento', id=id)
    
    # Se não for POST, mostra página de confirmação
    return render(request, 'confirmarexclusaoapartamento.html', {'apartamento': apartamento})

@login_required(login_url='/login/') 
@requer_consultor
def cadastro_consultor(request):
    if request.method == 'POST':
        form = ConsultorForm(request.POST, request.FILES)
        #print(form)
        if form.is_valid():
            form.save()
            return redirect('sucesso')
    else:
        form = ConsultorForm()
    
    return render(request, 'cadastro/formularioconsultor.html', {'form': form})

@login_required(login_url='/login/') 
@requer_consultor
def consulta_consultores(request):
    consultores = Consultor.objects.all().order_by('consultorNome')
    
    # Filtros
    nome = request.GET.get('nome')
    email = request.GET.get('email')
    
    if nome:
        consultores = consultores.filter(Q(consultorNome__icontains=nome))
    if email:
        consultores = consultores.filter(Q(consultorEmail__icontains=email))

    
    context = {
        'consultores': consultores,
        'filtros': {
            'consultorNome': nome or '',
            'consultorEmail': email or '',
        }
    }
    
    return render(request, 'consulta_consultores.html', context)

@login_required(login_url='/login/') 
@requer_consultor
def excluir_consultor(request, id):
    consultor = get_object_or_404(Consultor, id=id)
    
    if request.method == 'POST':
        try:
            consultor.delete()
            messages.success(request, 'Consultor excluído com sucesso!')
            return redirect('consulta_consultores')
        except Exception as e:
            messages.error(request, f'Erro ao excluir consultor: {str(e)}')
            return redirect('detalhes_consultor', id=id)
    
    # Se não for POST, mostra página de confirmação
    return render(request, 'confirmarexclusaoconsultor.html', {'consultor': consultor})

@login_required(login_url='/login/')
@requer_consultor
def detalhes_consultor(request, id):
    consultor = get_object_or_404(Consultor, id=id)
    return render(request, 'detalhes_consultor.html', {'consultor': consultor})

@login_required(login_url='/login/') 
@requer_consultor
def editar_consultor(request, id):
    consultor = get_object_or_404(Consultor, id=id)
    
    if request.method == 'POST':
        form = ConsultorForm(request.POST, request.FILES, instance=consultor)
        if form.is_valid():
            form.save()
            return redirect('detalhes_consultor', id=consultor.id)
    else:
        form = ConsultorForm(instance=consultor)
    
    return render(request, 'editar_consultor.html', {
        'form': form,
        'consultor': consultor
    })

@login_required(login_url='/login/') 
def cadastro_precliente(request):
    if request.method == 'POST':
        form = PreClienteForm(request.POST, request.FILES)
        #print(form)
        if form.is_valid():
            form.save()
            return redirect('sucesso')
    else:
        form = PreClienteForm()
    
    return render(request, 'cadastro/formularioprecliente.html', {'form': form})

@login_required(login_url='/login/')
def consulta_preclientes(request):
    # Obtém todos os clientes inicialmente
    consultor_id = request.session.get('consultor_id')
    if consultor_id:
        preclientes = PreCliente.objects.filter(Consultor = consultor_id).all().order_by('preclienteNome')
    else:
        preclientes = PreCliente.objects.all().order_by('preclienteNome')

    # Filtros
    nome = request.GET.get('nome')
    cpf = request.GET.get('cpf')
    
    if nome:
        preclientes = preclientes.filter(Q(preclienteNome__icontains=nome))
    if cpf:
        preclientes = preclientes.filter(Q(preclienteCpf__icontains=cpf))

    
    context = {
        'preclientes': preclientes,
        'filtros': {
            'preclienteNome': nome or '',
            'preclienteCpf': cpf or '',
        },
        'is_consultor': request.session.get('api_funcao') == 'CONSULTOR'
    }
    
    return render(request, 'consulta_precliente.html', context)

@login_required(login_url='/login/')
def detalhes_precliente(request, id):
    precliente = get_object_or_404(PreCliente, id=id)
    return render(request, 'detalhes_precliente.html', {'precliente': precliente})


@login_required(login_url='/login/')
def editar_precliente(request, id):
    precliente = get_object_or_404(PreCliente, id=id)
    
    if request.method == 'POST':
        form = PreClienteForm(request.POST, request.FILES, instance=precliente)
        if form.is_valid():
            form.save()
            return redirect('detalhes_precliente', id=precliente.id)
    else:
        form = PreClienteForm(instance=precliente)
    
    return render(request, 'editar_precliente.html', {
        'form': form,
        'precliente': precliente
    })

@login_required(login_url='/login/') 
def excluir_precliente(request, id):
    precliente = get_object_or_404(PreCliente, id=id)
    
    if request.method == 'POST':
        try:
            precliente.delete()
            messages.success(request, 'Pré-Cliente excluído com sucesso!')
            return redirect('consulta_preclientes')
        except Exception as e:
            messages.error(request, f'Erro ao excluir pré-cliente: {str(e)}')
            return redirect('detalhes_precliente', id=id)
    
    # Se não for POST, mostra página de confirmação
    return render(request, 'confirmar_exclusaoprecliente.html', {'precliente': precliente})

def converter_precliente(request, precliente_id):
    precliente = get_object_or_404(PreCliente, pk=precliente_id)
    #print(precliente)
    
    try:
        precliente = precliente.converter_para_cliente(
            consultor=request.user.consultor if hasattr(request.user, 'consultor') else None
        )
        messages.success(request, f'Pré-cliente convertido para cliente com sucesso!')
        return redirect('consulta_preclientes')
    except Exception as e:
        messages.error(request, f'Erro ao converter pré-cliente: {str(e)}')
        return redirect('consulta_preclientes')


def consulta_cpf(request):
    #print('consulta_cpf')
    if request.method == 'POST':
        cpf = request.POST.get('cpf', '').replace('.', '').replace('-', '')
        
        if not cpf.isdigit() or len(cpf) != 11:
            return JsonResponse({'error': 'CPF inválido'}, status=400)
        
        try:
            data = APIDataBuscaService.get_api_data(cpf)
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Método não permitido'}, status=405)

def consulta_view(request):
    return render(request, 'consulta.html')

def preencher_pdf(request, cliente_id):
    # Obtenha o template do banco de dados
    cliente = Cliente.objects.get(id=cliente_id)

    # Dados dinâmicos - pode vir de um formulário ou banco de dados
    nome = f"{cliente.nome}".replace("{", "").replace("}", "").replace("'", "")
    profissao = f"{cliente.profissao}".replace("{", "").replace("}", "").replace("'", "")
    estadocivil = f"{cliente.estcivil}".replace("{", "").replace("}", "").replace("'", "")
    rg = f"{cliente.rgrne}".replace("{", "").replace("}", "").replace("'", "")
    cpf = f"{cliente.cpf}".replace("{", "").replace("}", "").replace("'", "")
    email = f"{cliente.email}".replace("{", "").replace("}", "").replace("'", "")
    celular = f"{cliente.telefone}".replace("{", "").replace("}", "").replace("'", "")
    endereco = f"{cliente.endereco}".replace("{", "").replace("}", "").replace("'", "")
    nomeresidente = f"{cliente.nomeresidente}".replace("{", "").replace("}", "").replace("'", "")
    numerorg = f"{cliente.rgresidente}".replace("{", "").replace("}", "").replace("'", "")
    cpfresidente = f"{cliente.cpfresidente}".replace("{", "").replace("}", "").replace("'", "")
    enderecoresidente = f"{cliente.enderecoresidente}".replace("{", "").replace("}", "").replace("'", "")
    profissaoresidente  = f"{cliente.profissaoresidente}".replace("{", "").replace("}", "").replace("'", "")
    estadocivilresidente = f"{cliente.estadocivilresidente}".replace("{", "").replace("}", "").replace("'", "")
    celularresidente = f"{cliente.celularresidente}".replace("{", "").replace("}", "").replace("'", "")
    emailresidente = f"{cliente.emailresidente}".replace("{", "").replace("}", "").replace("'", "")
    apto = f"{cliente.apto}".replace("{", "").replace("}", "").replace("'", "")
    vaga = f"{cliente.vagaunidade}".replace("{", "").replace("}", "").replace("'", "")
    matricula = f"{cliente.matriculaunidade}".replace("{", "").replace("}", "").replace("'", "")
    condominio =f"{cliente.Condominio.condominionome}".replace("{", "").replace("}", "").replace("'", "")
    cnpjcondominio = f"{cliente.Condominio.condominiocnpj}".replace("{", "").replace("}", "").replace("'", "")
    enderecocondominio = f"{cliente.Condominio.condominioendereco}".replace("{", "").replace("}", "").replace("'", "")
    nriptu = f"{cliente.Condominio.condominiomatricula}".replace("{", "").replace("}", "").replace("'", "")
    datainicio = f"{cliente.iniciocontrato}".replace("{", "").replace("}", "").replace("'", "")
    valor = f"{cliente.vrunidade}".replace("{", "").replace("}", "").replace("'", "")
    prazocontrato = f"{cliente.prazocontrato}".replace("{", "").replace("}", "").replace("'", "")
    dia = datetime.now().day
    mes = datetime.now().month
    ano = datetime.now().year
    percdes = f"{cliente.percentualdesconto}".replace("{", "").replace("}", "").replace("'", "")
    iniciodesc = f"{cliente.datainiciodesconto}".replace("{", "").replace("}", "").replace("'", "")
    terminodesc = f"{cliente.dataterminodesconto}".replace("{", "").replace("}", "").replace("'", "")
    data_obj = datetime.strptime(datainicio, "%Y-%m-%d")
    data_formatada = data_obj.strftime("%d/%m/%Y")

    data_obj = datetime.strptime(iniciodesc, "%Y-%m-%d")
    iniciodescformat = data_obj.strftime("%d/%m/%Y")

    data_obj = datetime.strptime(terminodesc, "%Y-%m-%d")
    terminodescformat = data_obj.strftime("%d/%m/%Y")

    textoi1 = ''
    textoi11 = ''
    if cliente.percentualdesconto > 0:
        textoi1 = f"I.2. Desconto de Incentivo: A VILA 11 concede ao LOCATÁRIO desconto no valor do Aluguel, especificamente para o Período de Desconto de {iniciodescformat} a {terminodescformat}, conforme abaixo:"
        textoi11 = f"a) De {iniciodescformat} a {terminodescformat} de locação - {cliente.percentualdesconto} % de desconto sobre o valor do Aluguel mensal;"
    
    dadosdocondominio = f"{cliente.Condominio.condominionomecomercial} Sociedade Anônima, inscrita no CNPJ nº {cliente.Condominio.condominiocnpj} com endereço em {cliente.Condominio.condominioendereco}"
    meses_pt = {
        1: "Janeiro",
        2: "Fevereiro",
        3: "Março",
        4: "Abril",
        5: "Maio",
        6: "Junho",
        7: "Julho",
        8: "Agosto",
        9: "Setembro",
        10: "Outubro",
        11: "Novembro",
        12: "Dezembro"
    }
    
    nome_mes = meses_pt.get(mes, "Mês inválido")


    context = {
        'nome': nome,
        'profissão': profissao,
        'estadocivil': estadocivil,
        'rg': rg,
        'cpf': cpf,
        'email': email,
        'celular': celular,
        'endereco': endereco,
        'nomeresidente': nomeresidente,
        'numerorg': numerorg,
        'cpfresidente': cpfresidente,
        'enderecoresidente': enderecoresidente,
        'profissaoresidente' :  profissaoresidente,
        'estadocivilresidente' : estadocivilresidente,
        'celularresidente' : celularresidente,
        'emailresidente' : emailresidente,
        'nomeadministradora': 'Vila11',
        'cnpjadministradora': '37.232.210/0001-15',
        'contatoadministradora': 'Contato Vila11',
        'apto': apto,
        'vaga': vaga,
        'matricula': matricula,
        'condominio': condominio,
        'cnpjcondominio': cnpjcondominio,
        'Contato': 'Contato Vila11',
        'enderecocondominio': enderecocondominio,
        'nriptu': nriptu,
        'datainicio': data_formatada,
        'valor': valor,
        'prazocontrato': prazocontrato,
        'mesano': datetime.now().strftime("%m/%Y"),
        'dia': dia,
        'mes': nome_mes,
        'ano': ano,
        'clausulai1': textoi1,
        'clausulai11': textoi11,
        'dadoscondominio': dadosdocondominio
    }    

    try:
        # Caminho completo para o template
        template_path = "template.docx" #template.template_file.path
        
        # Carrega o template
        buffer = BytesIO()
        doc = DocxTemplate(template_path)
        
        # Substitui os placeholders
        doc.render(context)
        
        # Caminho para salvar o documento gerado
        output_filename = f'documento_gerado_{cliente_id}.docx'
        output_path = os.path.join(settings.MEDIA_ROOT, 'generated', output_filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Salva o documento
        doc.save(output_path)
        buffer.seek(0)
        # Salva o arquivo no campo documentacaoenviada
        cliente.documentacaoenviada.save(output_filename, buffer)
        cliente.save()
        buffer.seek(0)
        # Retorna o arquivo para download
        return FileResponse(open(output_path, 'rb'), 
                         as_attachment=True, 
                         filename=output_filename)
    
    except Exception as e:
        return HttpResponse(f"Erro ao gerar documento: {str(e)}", status=500)
    
def visualizar_documento(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    
    # Verifica se o arquivo existe
    if not cliente.documentacaoenviada:
        raise Http404("Documento não encontrado")
    
    # Pega a extensão do arquivo
    _, ext = os.path.splitext(cliente.documentacaoenviada.name)
    ext = ext.lower()
    
    # Verifica se é um arquivo Word
    if ext not in ['.doc', '.docx']:
        return render(request, 'erro.html', {
            'mensagem': 'O arquivo não é um documento Word válido'
        })
    
    # Se for DOCX, podemos tentar converter para HTML para visualização
    #print(ext)
    #print(cliente.documentacaoenviada.path)
    if ext == '.docx':
        #print('dentro')
        try:
            #print('try')
            import docx2txt
            texto = docx2txt.process(cliente.documentacaoenviada.path)
            #print('texto: ' + texto)
            return render(request, 'visualizar_word.html', {
                'cliente': cliente,
                'conteudo': texto,
                'tipo': 'docx'
            })
        except ImportError:
            #print('except')
            # Se docx2txt não estiver instalado, faz download
            pass
        except Exception as e:
            #print(Exception)
            #print('exception')
            return render(request, 'erro.html', {
                'mensagem': f'Erro ao processar documento: {str(e)}'
            })
    
    # Para arquivos .doc ou se a conversão falhar
    return render(request, 'visualizar_word.html', {
        'cliente': cliente,
        'tipo': 'download'
    })

def get_dados_condominio(request):
    condominio_id = request.GET.get('condominio_id')
    
    try:
        condominio = Condominio.objects.get(id=condominio_id)
        apartamentos = Apartamento.objects.filter(Condominio_id=condominio_id).values('id', 'apartamentonro')
        
        data = {
            'condominionome': condominio.condominionome,
            'condominiocnpj': condominio.condominiocnpj,
            'condominiomatricula': condominio.condominiomatricula,
            'condominioendereco': condominio.condominioendereco,
            'apartamentos': list(apartamentos)
        }
        return JsonResponse(data)
    
    except Condominio.DoesNotExist:
        return JsonResponse({'error': 'Condomínio não encontrado'}, status=404)

def get_condominio_completo(request):
    condominio_id = request.GET.get('condominio_id')
    
    try:
        condominio = Condominio.objects.get(id=condominio_id)
        apartamentos = Apartamento.objects.filter(Condominio_id=condominio_id).values(
            'id', 
            'apartamentonro',
            'apartamentovagas',
            'apartamentoiptu',
            'apartamentovrunidade'
        )
        
        response_data = {
            'condominio': model_to_dict(condominio),
            'apartamentos': list(apartamentos)
        }
        return JsonResponse(response_data)
    
    except Condominio.DoesNotExist:
        return JsonResponse({'error': 'Condomínio não encontrado'}, status=404)

def get_apartamentos(request):
    condominio_id = request.GET.get('condominio_id')
    #apartamentos = Apartamento.objects.filter(Condominio_id=condominio_id).values('id', 'apartamentonro', 'apartamentovagas', 'apartamentoiptu', 'apartamentovrunidade')
    #return JsonResponse(list(apartamentos), safe=False)
    apartamentos = Apartamento.objects.filter(condominio_id=condominio_id)
    options = '<option value="">Selecione um apartamento</option>'
    for apto in apartamentos:
        options += f'<option value="{apto.id}">{apto.apartamentonro} - {apto.apartamentovagas or ""}</option>'
    return JsonResponse(options, safe=False)


User = get_user_model()
logger = logging.getLogger(__name__)
def login_view(request):
    #print('entrou no Login')
    if request.user.is_authenticated:
        return redirect('consulta_clientes')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, 'Usuário e senha são obrigatórios')
            return render(request, 'registration/login.html')

        try:
            # 1. Primeiro valida com a API externa
            response = requests.post(
                #'http://3.143.172.37:8001/api/login/',
                'http://localhost:8001/api/login/',
                json={'username': username, 'password': password},
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            #print(response)
            if response.status_code != 200:
                #print('status diferente de 200')
                #print(response.status_code)
                messages.error(request, 'Credenciais inválidas')
                return render(request, 'registration/login.html')
                
            token_data = response.json()
            #print(token_data)
            # 2. Verifica/Cria usuário local
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'is_active': True,
                    'is_staff': False,  # Ajuste conforme necessário
                    'is_superuser': False
                }
            )
            
            if created:
                logger.info(f'Novo usuário criado: {username}')
                user.set_unusable_password()  # Não usaremos senha local
                user.save()
            
            # 3. Autentica o usuário (sem verificar senha local)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            
            # 4. Armazena o token e função na sessão
            request.session['api_token'] = token_data.get('token')
            response_dados = requests.get(
                #f'http://3.143.172.37:8001/api/usuario-por-email/?nomeusuario={username}',
                f'http://localhost:8001/api/usuario-por-email/?nomeusuario={username}',
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            if response_dados.status_code == 200:
                dados = response_dados.json()
                funcao = dados["usuarioFuncao"]
                email = dados["usuarioEmail"]
                if funcao == 'CONSULTOR':
                    request.session['is_consultor'] = True
                    request.session['api_funcao'] = funcao
                    consultor = Consultor.objects.filter(consultorEmail=email).first()
                    consultor_id = consultor.pk
                    #print(consultor_id)
                    request.session['email'] = email
                    request.session['consultor_id'] = consultor_id
                else:
                    request.session['is_consultor'] = False
                
            else:
                print(f"Erro {response_dados.status_code}: {response_dados.text}")
            
            #Grava o log de acesso
            logacesso = LogAcesso(
                logacessoUsuario = username
            )
            logacesso.save()

            return redirect(request.GET.get('next', 'consulta_clientes'))
            
        except RequestException as e:
            logger.error(f'Erro na API de autenticação: {str(e)}')
            messages.error(request, 'Erro ao conectar com o servidor de autenticação')
    
    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Você foi desconectado com sucesso')
    return redirect('login')

class CondominioKPIDashboard(TemplateView):
    template_name = 'condominio/kpi_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hoje = datetime.now().date()
        # KPIs principais
        context['total_condominios'] = Condominio.objects.count()
        context['total_apartamentos'] = Apartamento.objects.count()
        context['total_consultores'] = Consultor.objects.count()     
        context['total_preclientes'] = PreCliente.objects.count()
        context['total_clientes'] = Cliente.objects.count()
        context['total_acessos'] = LogAcesso.objects.filter(logacessoData=hoje).count()


        #grafico preclientes aprovados
        # Preparar os dados para o gráfico
        labels = []
        data = []
        colors = []

        # Adicionar contagem para valores nulos (não avaliados)
        nao_apto = PreCliente.objects.filter(preclienteScore__lte = 700
                                             ).filter(
                                                 ~Q(preclienteApontamentos='') | Q(preclienteApontamentos__isnull=False)
                                             ).count()
        if nao_apto > 0:
            labels.append('Não Apto')
            data.append(nao_apto)
            colors.append('#F44336')  # Vermelho

        apto = PreCliente.objects.filter(
                                        preclienteScore__gte=700
                                        ).filter(
                                        Q(preclienteApontamentos='') | Q(preclienteApontamentos__isnull=True)
                                        ).count()
        if apto > 0:
            labels.append('Apto')
            data.append(apto)
            colors.append('#4CAF50')  # Verde
        
        context['gr_precliente'] = {
            'labels': labels,
            'data': data,
            'colors': colors,
            'total': sum(data),
        }
        #print(context)

        # grafico de acessos por usuário/dia
        acessos_por_usuario = (
            LogAcesso.objects
            .filter(logacessoData=hoje)
            .values('logacessoUsuario')
            .annotate(total=Count('id'))
            .order_by('-total')
        )

        # Preparar dados para o gráfico de barras
        user_labels = [item['logacessoUsuario'] for item in acessos_por_usuario]
        user_data = [item['total'] for item in acessos_por_usuario]

        context['gr_acessos_usuarios'] = {
            'labels': user_labels,
            'data': user_data,
            }    
        
        return context

#@require_http_methods(["POST"])  # Agora só aceita POST
def assinar_contrato(request, cliente_id):
    # Obtenha o template do banco de dados
    cliente = Cliente.objects.get(id=cliente_id)
    nomedocumento = f"Contrato de Locação - {cliente.nome} - {cliente.Condominio.condominionome}"
    document_data = {
        "signature_list": [
            {
                "service": "lexiosign",
                "titulo": nomedocumento,
                "signers": [
                    {
                        "nome": cliente.nome,
                        "email": cliente.email,
                        "funcao": "Cliente"
                    },
                    {
                        "nome": "Isadora Romão",
                        "email": "isadora.romao@vila11.com.br",
                        "funcao": "Testemunha"
                    },
                    {
                        "nome": "Carla Viana",
                        "email": "carla.viana@vila11.com.br",
                        "funcao": "Testemunha"
                    },
                    {
                        "nome": "Jorge Luiz Bernardo de moraes",
                        "email": "jorge.moraes@vila11.com.br",
                        "funcao": "Representante Legal"
                    },
                    {
                        "nome": "Roberto Sergio Dib",
                        "email": "roberto.dib@vila11.com.br",
                        "funcao": "Representante Legal"
                    }
                ],
                "send_email": True,
                "order_by": False,
                "lembrete": 3,
                "engine_campos": {
                    "Landlord": cliente.Condominio.condominionomecomercial, 
                    "Type": "Sociedade de responsabilidade limitada", 
                    "Cnpj": cliente.Condominio.condominiocnpj, 
                    "AddressLandlord": cliente.Condominio.condominioendereco, 
                    "IndicatedPerson": cliente.nome, 
                    "EmailPerson": cliente.email, 
                    "Lessee": "1", 
                    "NameOne": cliente.email, 
                    "ProfessionOne": cliente.profissao, 
                    "MaritalStatOne": cliente.estcivil, 
                    "RgOne": cliente.rgrne, 
                    "CpfOne": cliente.cpf, 
                    "EmailOne": cliente.email, 
                    "CelOne": cliente.telefone, 
                    "AddressOne": cliente.endereco, 
                    "NameTwo": "", 
                    "ProfessionTwo": "", 
                    "MaritalStatTwo": "", 
                    "RgTwo": "", 
                    "CpfTwo": "", 
                    "EmailTwo": "", 
                    "CelTwo": "", 
                    "AddressTwo": "", 
                    "NameThree": "", 
                    "ProfessionThree": "", 
                    "MaritalStatThree": "", 
                    "RgThree": "", 
                    "CpfThree": "", 
                    "EmailThree": "", 
                    "CelThree": "", 
                    "AddressThree": "", 
                    "NameFour": "", 
                    "ProfessionFour": "", 
                    "MaritalStatFour": "", 
                    "RgFour": "", 
                    "CpfFour": "", 
                    "EmailFour": "", 
                    "CelFour": "", 
                    "AddressFour": "", 
                    "NameFive": "", 
                    "ProfessionFive": "", 
                    "MaritalStatFive": "", 
                    "RgFive": "", 
                    "CpfFive": "", 
                    "EmailFive": "", 
                    "CelFive": "", 
                    "AddressFive": "", 
                    "Residents": "1", 
                    "ResNameOne": cliente.nomeresidente, 
                    "ResRgOne": cliente.rgresidente, 
                    "ResCpfOne": cliente.cpfresidente, 
                    "ResNameTwo": "", 
                    "ResRgTwo": "", 
                    "ResCpfTwo": "", 
                    "ResNameThree": "", 
                    "ResRgThree": "", 
                    "ResCpfThree": "", 
                    "ResNameFour": "", 
                    "ResRgFour": "", 
                    "ResCpfFour": "", 
                    "AdmName": cliente.Condominio.condominionomecomercial, 
                    "AdmCnpj": cliente.Condominio.condominiocnpj, 
                    "AdmCel": "(11) 99999-9999", 
                    "Apartment": cliente.apto, 
                    "CondoName": cliente.Condominio.condominionome, 
                    "Registration": cliente.Condominio.condominiomatricula, 
                    "ContactCondo": "(11) 99999-9999", 
                    "CnpjCondo": cliente.Condominio.condominiocnpj, 
                    "PropertyAddress": cliente.Condominio.condominioendereco, 
                    "Iptu": cliente.Condominio.condominiomatricula, 
                    "RentMonth": str(cliente.vrunidade), 
                    "DataBase": datetime.now().strftime("%Y%m%d"), #cliente.iniciocontrato.strftime("%Y%m%d"), 
                    "DataSig": datetime.now().strftime("%Y%m%d"), 
                    "WitName1": "", 
                    "WitAdress1": "", 
                    "WitRg1": "", 
                    "WitName2": "", 
                    "WitAdress2": "", 
                    "WitRg2": ""
                }
            }
        ]
    }
    # URL da API
    url = "https://app.lexio.legal/api/generate_form_document_v2/Vila11LocacaoQuadroResumoTeste"
    
    # Headers com o token de autenticação
    headers = {
        "lexiotoken": '8e3d3c2bc7bce9c379e4976c4de696e7a73eb1888f6d19182c3741269fcb6b7e',
        "Content-Type": "application/json"
    }
    try:
        # Faz a requisição POST
        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(document_data))  # Convertemos o dict para JSON string
        
        #print(response)
        # Verifica se a requisição foi bem sucedida
        if response.status_code == 200:
            #print(response.json())
            resposta = response.json()
            process_id = resposta["sent"][0]["process_id"]
            #print(process_id)
            cliente.processoassinaturaid = process_id
            cliente.save()
            #print(JsonResponse(resposta))
            return redirect(request.GET.get('next', 'consulta_clientes'))
            #return JsonResponse(resposta)  # Retorna a resposta da API como JSON
             
        else:
            #print(f"Erro na requisição: Status {response.status_code}")
            #print(f"Resposta: {response.text}")
            return JsonResponse({
                "erro": f"Erro na requisição: {response.status_code}",
                "mensagem": response.text
            }, status=response.status_code)

    except requests.exceptions.RequestException as e:
        #print(f"Erro ao conectar com a API: {str(e)}")
        return JsonResponse({"erro": "Falha na conexão com a API", "mensagem": str(e)}, status=500)
    except json.JSONDecodeError as e:
        #print(f"Erro ao decodificar a resposta JSON: {str(e)}")
        return JsonResponse({"erro": "Erro ao decodificar JSON", "mensagem": str(e)}, status=500)

logger = logging.getLogger(__name__)
@csrf_exempt  # Para permitir requisições externas (sem CSRF token)
def webhook_receiver(request):
    if request.method == "POST":
        try:
            payload = json.loads(request.body)
            data = json.loads(request.body)
            #logger.info(f"Webhook recebido: {payload}")
            #print(f"Webhook recebido: {payload}")
            processo_id = data.get('payload', {}).get('process_id', None)
            doc_download = data.get('payload', {}).get('download', None)
            doc_status = data["payload"]["contrato"]["status"]
            enderecowebhook = data["payload"]["document"]["signers"][0]["signer_link"]
            #data.get('payload', {}).get('signer_link', None)
            #print(enderecowebhook)
            #print(doc_status)
            #print(f"processo_id: {processo_id}")
            cliente = Cliente.objects.filter(processoassinaturaid=processo_id).first()
            if cliente.Consultor.pk:
                consultor_id = cliente.Consultor.pk
            else:
                consultor_id = None
            #print('gravar notificacao: ' + str(consultor_id))
            #print(cliente)
            if cliente is None:
                logger.error(f"Cliente não encontrado para o process_id: {payload.get('process_id')}")
                return JsonResponse({"erro": "Cliente não encontrado"}, status=404)
                
            if doc_status == 'assinado':
                cliente.documentacaoassinada = True
                cliente.datahoraassinatura = datetime.now()
                # Salva o documento assinado
                if doc_download:
                    try:
                        response = requests.get(doc_download)
                        if response.status_code == 200:
                            # Salva o documento assinado no campo documentacaoassinada
                            cliente.documentacaoenviada.save(
                                f"Contrato_Assinado_{cliente.nome}.pdf",
                                ContentFile(response.content)
                            )
                        else:
                            logger.error(f"Erro ao baixar o documento: {response.status_code}")
                    except requests.RequestException as e:
                        logger.error(f"Erro ao baixar o documento: {str(e)}")
            else:
                cliente.documentacaoassinada = False

            cliente.enderecowebhook = enderecowebhook
            cliente.statusassinatura = doc_status
            cliente.save()
            #grava a notificação de recebimento do webhook
            notificacao = Notificacao(
                    NotificacaoTitulo = 'Contrato assinado:' + cliente.nome if doc_status == 'assinado' else 'Assinatura de Contrato: ' + cliente.nome,
                    NotificacaoData = datetime.now(),
                    NotificacaoDescricao = enderecowebhook,
                    NotificacaoTipo = 'A',
                    NotificacaoLido = False,
                    Consultor = Consultor.objects.get(id=consultor_id)
            )
            notificacao.save()
            return JsonResponse({"status": "sucesso"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"erro": "JSON inválido"}, status=400)

    return JsonResponse({"erro": "Método não permitido"}, status=405)


def notificacoes_view(request):
    consultor_id = request.session.get('consultor_id')
    #print(consultor_id)
    if consultor_id:
        notificacoes = Notificacao.objects.filter(
            Consultor = consultor_id, 
            NotificacaoLido=False
            ).order_by('-NotificacaoData')[:10]
    else:
        notificacoes = Notificacao.objects.filter(NotificacaoLido=False).order_by('-NotificacaoData')[:10]

    #print(notificacoes)
    notificacoes_nao_lidas = notificacoes.filter(NotificacaoLido=False)
    return render(request, 'notificacoes.html', {
        'notificacoes': notificacoes,
        'notificacoes_nao_lidas': notificacoes_nao_lidas.count()
    })

def notificacoes_ajax(request):
    consultor_id = request.session.get('consultor_id')
    #print('ajax: ' + str(consultor_id))
    if consultor_id:
        notificacoes = Notificacao.objects.filter(
            Consultor = consultor_id, 
            NotificacaoLido=False
            ).order_by('-NotificacaoData')[:10]
    else:
        notificacoes = Notificacao.objects.filter(NotificacaoLido=False).order_by('-NotificacaoData')[:10]

    data = []
    for n in notificacoes:
        data.append({
            'id': n.id,
            'titulo': n.NotificacaoTitulo,
            'descricao': n.NotificacaoDescricao,
            'tipo': n.get_NotificacaoTipo_display(),
            'data': n.NotificacaoData.strftime("%d/%m/%Y %H:%M"),
            'lido': n.NotificacaoLido
        })

    #print(data)

    return JsonResponse({'notificacoes': data})

@csrf_exempt  # ou use o token CSRF no JavaScript, veja nota abaixo
def marcar_notificacao_lida(request):
    if request.method == 'POST':
        id_notificacao = request.POST.get('id')
        #print(id_notificacao)
        if not id_notificacao:
            return JsonResponse({'status': 'erro', 'mensagem': 'ID da notificação não fornecido'})
        try:
            notificacao = Notificacao.objects.get(id=id_notificacao)
            notificacao.NotificacaoLido = True
            notificacao.save()
            return JsonResponse({'status': 'ok'})
        except Notificacao.DoesNotExist:
            return JsonResponse({'status': 'erro', 'mensagem': 'Notificação não encontrada'})
    return JsonResponse({'status': 'erro', 'mensagem': 'Requisição inválida'})

def criar_cadastro(request):
    #print('entrou no criar_cadastro')
    if request.method == 'POST':
        form = PreCliente(request.POST)
        if form.is_valid():
            PreCliente = form.save(commit=False)
            consultor_id = request.session.get('consultor_id')
            if consultor_id:
                PreCliente.Consultor = consultor_id
            PreCliente.save()
            return redirect('cadastro_sucesso')
    else:
        form = PreCliente()

    return render(request, 'consulta_preclientes.html', {'form': form})

class ClienteListView(generics.ListAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class NotificacaoListView(generics.ListAPIView):
    queryset = Notificacao.objects.all()
    serializer_class = NotificacaoSerializer

class ClienteCrudViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteCrudSerializer