from django.shortcuts import redirect, render

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
