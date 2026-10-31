from django.urls import path

from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('cardapio/', views.cardapio, name='cardapio'),
    path('clientes/', views.clientes, name='clientes'),
    path('pedidos/', views.lista_pedidos, name='pedidos'),
    path('produtos/novo/', views.novo_produto, name='novo_produto'),
    path('produtos/<int:id>/editar/', views.editar_produto, name='editar_produto'),
    path('pedidos/novo/', views.novo_pedido, name='novo_pedido'),
    path('clientes/novo/', views.novo_cliente, name='novo_cliente'),
]
