from django.shortcuts import get_object_or_404, redirect, render

from .forms import ClienteForm, PedidoForm, ProdutoForm
from .models import Cliente, Pedido, Produto


def inicio(request):
    return redirect('cardapio')


def cardapio(request):
    produtos = Produto.objects.all()
    return render(request, 'pedidos/cardapio.html', {'produtos': produtos})


def clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'pedidos/clientes.html', {'clientes': clientes})


def lista_pedidos(request):
    pedidos = Pedido.objects.select_related('cliente', 'produto').all()
    return render(request, 'pedidos/lista_pedidos.html', {'pedidos': pedidos})


def novo_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cardapio')
    else:
        form = ProdutoForm()
    return render(request, 'pedidos/produto_form.html', {'form': form})


def editar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('cardapio')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'pedidos/produto_form.html', {'form': form})


def novo_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pedidos')
    else:
        form = PedidoForm()
    return render(request, 'pedidos/pedido_form.html', {'form': form})


def novo_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clientes')
    else:
        form = ClienteForm()
    return render(request, 'pedidos/cliente_form.html', {'form': form})
