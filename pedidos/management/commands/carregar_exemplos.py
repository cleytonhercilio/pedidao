from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from pedidos.models import Cliente, Pedido, Produto


class Command(BaseCommand):
    help = 'Carrega os exemplos das aulas sem apagar dados ou duplicar os exemplos.'

    @transaction.atomic
    def handle(self, *args, **options):
        clientes = []
        for nome, telefone in [
            ('Ana Souza', '81 99999-0001'),
            ('Bruno Lima', '81 99999-0002'),
            ('Carla Dias', '81 99999-0003'),
        ]:
            cliente, _ = Cliente.objects.get_or_create(nome=nome, telefone=telefone)
            clientes.append(cliente)

        produtos = []
        for nome, preco in [
            ('X-Tudo', '18.90'),
            ('Coca-Cola lata', '6.00'),
            ('Batata frita', '12.50'),
        ]:
            produto, _ = Produto.objects.get_or_create(
                nome=nome, defaults={'preco': Decimal(preco)}
            )
            produtos.append(produto)

        for cliente, produto, quantidade in zip(clientes, produtos, [2, 1, 3]):
            Pedido.objects.get_or_create(
                cliente=cliente, produto=produto, quantidade=quantidade
            )
        self.stdout.write(self.style.SUCCESS('Exemplos das aulas carregados.'))
