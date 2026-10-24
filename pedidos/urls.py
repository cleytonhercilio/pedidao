from django.urls import path

from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('cardapio/', views.cardapio, name='cardapio'),
    path('clientes/', views.clientes, name='clientes'),
    path('pedidos/', views.lista_pedidos, name='pedidos'),
]
