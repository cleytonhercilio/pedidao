from decimal import Decimal
from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.db.models.deletion import ProtectedError
from django.test import TestCase
from django.urls import reverse

from .models import Cliente, Pedido, Produto


class PedidaoTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cliente = Cliente.objects.create(nome='Ana Souza', telefone='81 99999-0001')
        cls.produto = Produto.objects.create(nome='X-Tudo', preco=Decimal('18.90'))
        cls.pedido = Pedido.objects.create(
            cliente=cls.cliente, produto=cls.produto, quantidade=2
        )

    def test_paginas_dados_e_menu(self):
        paginas = {
            'cardapio': ['X-Tudo', '18,90'],
            'clientes': ['Ana Souza', '81 99999-0001'],
            'pedidos': ['Ana Souza pediu <span class="quantidade">2x</span> X-Tudo', '18,90'],
        }
        for pagina, textos in paginas.items():
            with self.subTest(pagina=pagina):
                resposta = self.client.get(reverse(pagina))
                for texto in textos:
                    self.assertContains(resposta, texto)
                for destino in paginas:
                    self.assertContains(resposta, f'href="{reverse(destino)}"')

    def test_inicio_redireciona_para_cardapio(self):
        self.assertRedirects(self.client.get('/'), reverse('cardapio'))

    def test_paginas_sem_registros(self):
        Pedido.objects.all().delete()
        Cliente.objects.all().delete()
        Produto.objects.all().delete()
        for pagina, mensagem in [
            ('cardapio', 'Nenhum produto cadastrado.'),
            ('clientes', 'Nenhum cliente cadastrado.'),
            ('pedidos', 'Nenhum pedido cadastrado.'),
        ]:
            with self.subTest(pagina=pagina):
                self.assertContains(self.client.get(reverse(pagina)), mensagem)

    def test_excluir_cliente_remove_pedido(self):
        self.cliente.delete()
        self.assertFalse(Pedido.objects.exists())
        self.assertTrue(Produto.objects.filter(pk=self.produto.pk).exists())

    def test_produto_vendido_protegido(self):
        with self.assertRaises(ProtectedError):
            self.produto.delete()
        self.assertTrue(Pedido.objects.filter(pk=self.pedido.pk).exists())

    def test_pedido_quantidade_padrao_e_representacao(self):
        pedido = Pedido.objects.create(cliente=self.cliente, produto=self.produto)
        self.assertEqual(pedido.quantidade, 1)
        self.assertEqual(str(pedido), f'Pedido {pedido.pk} - Ana Souza')
        self.assertEqual(str(self.cliente), 'Ana Souza')
        self.assertEqual(str(self.produto), 'X-Tudo')

    def test_admin_exige_login_e_permite_cadastro(self):
        url = reverse('admin:pedidos_pedido_add')
        self.assertEqual(self.client.get(url).status_code, 302)
        usuario = get_user_model().objects.create_superuser(
            username='teste', password='senha-apenas-para-teste'
        )
        self.client.force_login(usuario)
        for model in ['cliente', 'produto', 'pedido']:
            self.assertEqual(
                self.client.get(reverse(f'admin:pedidos_{model}_changelist')).status_code,
                200,
            )
        resposta = self.client.post(url, {
            'cliente': self.cliente.pk, 'produto': self.produto.pk, 'quantidade': 3,
            '_save': 'Salvar',
        })
        self.assertEqual(resposta.status_code, 302)
        self.assertTrue(Pedido.objects.filter(quantidade=3).exists())

    def test_exemplos_nao_duplicam_nem_alteram_precos(self):
        self.produto.preco = Decimal('20.00')
        self.produto.save()
        for _ in range(2):
            call_command('carregar_exemplos', stdout=StringIO())
        self.assertEqual(Cliente.objects.count(), 3)
        self.assertEqual(Produto.objects.count(), 3)
        self.assertEqual(Pedido.objects.count(), 3)
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.preco, Decimal('20.00'))

    def test_formularios_abrem_vazios_com_post_e_carimbo(self):
        for pagina in ['novo_produto', 'novo_pedido', 'novo_cliente']:
            with self.subTest(pagina=pagina):
                resposta = self.client.get(reverse(pagina))
                self.assertContains(resposta, '<form method="post">')
                self.assertContains(resposta, 'csrfmiddlewaretoken')

    def test_links_de_cadastro_nas_listas(self):
        for lista, cadastro in [
            ('cardapio', 'novo_produto'),
            ('pedidos', 'novo_pedido'),
            ('clientes', 'novo_cliente'),
        ]:
            with self.subTest(lista=lista):
                self.assertContains(self.client.get(reverse(lista)), f'href="{reverse(cadastro)}"')

    def test_cadastrar_produto_pelo_site(self):
        resposta = self.client.post(reverse('novo_produto'), {'nome': 'Misto Quente', 'preco': '9.50'})
        self.assertRedirects(resposta, reverse('cardapio'))
        self.assertTrue(Produto.objects.filter(nome='Misto Quente', preco=Decimal('9.50')).exists())

    def test_preco_impossivel_volta_com_erro(self):
        resposta = self.client.post(reverse('novo_produto'), {'nome': 'Combo Família', 'preco': '12345'})
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'Combo Família')
        self.assertContains(resposta, 'errorlist')
        self.assertFalse(Produto.objects.filter(nome='Combo Família').exists())

    def test_cadastrar_pedido_pelo_site(self):
        resposta = self.client.post(reverse('novo_pedido'), {
            'cliente': self.cliente.pk, 'produto': self.produto.pk, 'quantidade': 5,
        })
        self.assertRedirects(resposta, reverse('pedidos'))
        self.assertTrue(Pedido.objects.filter(cliente=self.cliente, quantidade=5).exists())

    def test_pedido_oferece_clientes_existentes(self):
        resposta = self.client.get(reverse('novo_pedido'))
        self.assertContains(resposta, '<select name="cliente"')
        self.assertContains(resposta, f'<option value="{self.cliente.pk}">Ana Souza</option>')

    def test_cadastrar_cliente_pelo_site(self):
        resposta = self.client.post(reverse('novo_cliente'), {'nome': 'Bruno', 'telefone': '81 98888-0000'})
        self.assertRedirects(resposta, reverse('clientes'))
        self.assertTrue(Cliente.objects.filter(nome='Bruno').exists())

    def test_editar_produto_altera_o_mesmo_registro(self):
        url = reverse('editar_produto', args=[self.produto.pk])
        self.assertContains(self.client.get(url), 'value="X-Tudo"')
        resposta = self.client.post(url, {'nome': 'X-Tudo Duplo', 'preco': '24.00'})
        self.assertRedirects(resposta, reverse('cardapio'))
        self.assertEqual(Produto.objects.count(), 1)
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.nome, 'X-Tudo Duplo')

    def test_editar_produto_inexistente(self):
        self.assertEqual(self.client.get(reverse('editar_produto', args=[999])).status_code, 404)
