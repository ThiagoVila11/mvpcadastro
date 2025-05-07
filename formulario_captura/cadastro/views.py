from django.shortcuts import render, redirect
from .forms import ClienteForm, CondominioForm, ApartamentoForm, ConsultorForm
from .models import Cliente, Condominio, Apartamento, Consultor
from django.db.models import Q
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
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


def cadastro_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('sucesso')
    else:
        form = ClienteForm()
    
    return render(request, 'cadastro/formulario.html', {'form': form})

def sucesso(request):
    return render(request, 'cadastro/sucesso.html')

def consulta_clientes(request):
    # Obtém todos os clientes inicialmente
    clientes = Cliente.objects.all().order_by('-data_cadastro')
    
    # Filtros
    nome = request.GET.get('nome')
    cpf = request.GET.get('cpf')
    unidade = request.GET.get('unidade')
    apto = request.GET.get('apto')
    
    if nome:
        clientes = clientes.filter(Q(nome__icontains=nome))
    if cpf:
        clientes = clientes.filter(Q(cpf__icontains=cpf))
    if unidade:
        clientes = clientes.filter(unidade=unidade)
    if apto:
        clientes = clientes.filter(apto=apto)
    
    # Obter opções para os selects
    unidades = Cliente.unidades
    
    context = {
        'clientes': clientes,
        'unidades': unidades,
        'filtros': {
            'nome': nome or '',
            'cpf': cpf or '',
            'unidade': unidade or '',
            'apto': apto or '',
        }
    }
    
    return render(request, 'consulta_clientes.html', context)

def detalhes_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    return render(request, 'detalhes_cliente.html', {'cliente': cliente})

def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    
    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('detalhes_cliente', id=cliente.id)
    else:
        form = ClienteForm(instance=cliente)
    
    return render(request, 'editar_cliente.html', {
        'form': form,
        'cliente': cliente
    })

def cadastro_condominio(request):
    if request.method == 'POST':
        form = CondominioForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('sucesso')
    else:
        form = CondominioForm()
    
    return render(request, 'cadastro/formulariocondominio.html', {'form': form})

def cadastro_apartamento(request):
    if request.method == 'POST':
        form = ApartamentoForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('sucesso')
    else:
        form = ApartamentoForm()
    
    return render(request, 'cadastro/formularioapartamento.html', {'form': form})

def cadastro_consultor(request):
    if request.method == 'POST':
        form = ConsultorForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('sucesso')
    else:
        form = ConsultorForm()
    
    return render(request, 'cadastro/formularioconsultor.html', {'form': form})

def consulta_cpf(request):
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
    apto = f"{cliente.apto}".replace("{", "").replace("}", "").replace("'", "")
    vaga = f"{cliente.vaga}".replace("{", "").replace("}", "").replace("'", "")
    matricula = f"{cliente.matriculaunidade}".replace("{", "").replace("}", "").replace("'", "")
    condominio =f"{cliente.nomeunidade}".replace("{", "").replace("}", "").replace("'", "")
    cnpjcondominio = f"{cliente.cnpjunidade}".replace("{", "").replace("}", "").replace("'", "")
    enderecocondominio = f"{cliente.enderecounidade}".replace("{", "").replace("}", "").replace("'", "")
    nriptu = f"{cliente.nriptuunidade}".replace("{", "").replace("}", "").replace("'", "")
    datainicio = f"{cliente.data_cadastro}".replace("{", "").replace("}", "").replace("'", "")
    valor = f"{cliente.vrunidade}".replace("{", "").replace("}", "").replace("'", "")
    dia = datetime.now().day
    mes = datetime.now().month
    ano = datetime.now().year

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
        'datainicio': datainicio,
        'valor': valor,
        'mesano': datetime.now().strftime("%m/%Y"),
        'dia': dia,
        'mes': mes,
        'ano': ano,
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
    print(ext)
    print(cliente.documentacaoenviada.path)
    if ext == '.docx':
        print('dentro')
        try:
            print('try')
            import docx2txt
            texto = docx2txt.process(cliente.documentacaoenviada.path)
            print('texto: ' + texto)
            return render(request, 'visualizar_word.html', {
                'cliente': cliente,
                'conteudo': texto,
                'tipo': 'docx'
            })
        except ImportError:
            print('except')
            # Se docx2txt não estiver instalado, faz download
            pass
        except Exception as e:
            print(Exception)
            print('exception')
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
    apartamentos = Apartamento.objects.filter(Condominio_id=condominio_id).values('id', 'apartamentonro', 'apartamentovagas', 'apartamentoiptu', 'apartamentovrunidade')
    return JsonResponse(list(apartamentos), safe=False)