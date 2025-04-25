from django.shortcuts import render, redirect
from .forms import ClienteForm
from .models import Cliente
from django.db.models import Q
from django.shortcuts import get_object_or_404

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