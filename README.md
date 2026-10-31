# Pedidão

Sistema de pedidos de uma lanchonete, implementado até o Sábado 5 dos materiais do Prof. Cleyton.
O projeto de configurações se chama `setup` neste repositório; corresponde à pasta `pedidao` dos slides.

## O que faltava e foi implementado

| Aula | Implementação |
| --- | --- |
| Sábado 1 | Correção de `pedido` para `pedidos` em INSTALLED_APPS; Cliente com nome e telefone; registro no Admin; migração e exemplos. |
| Sábado 2 | Produto com nome e preço decimal; Admin; URLs do projeto e app; views e templates de `/cardapio/` e `/clientes/`. |
| Sábado 3 | Pedido com cliente, produto e quantidade; Admin; `/pedidos/`; menu com rotas nomeadas nas três páginas. |
| Sábado 4 | Menu compartilhado no `base.html`; três páginas com `extends` e `block conteudo`; CSS em `static/pedidos/style.css`; cartões e destaque de preço e quantidade. |
| Sábado 5 | `forms.py` com `ProdutoForm` e `PedidoForm`; páginas `/produtos/novo/` e `/pedidos/novo/` com `method="post"` e `{% csrf_token %}`; views que tratam GET e POST, validam com `is_valid()` e redirecionam; links "+ Novo" no cardápio e na lista de pedidos. Degraus: `/clientes/novo/` e edição de produto em `/produtos/<id>/editar/` com `instance=`. |

Também foram incluídas as extensões dos slides: mensagens de lista vazia e preço unitário do produto na lista de pedidos.
A raiz `/` redireciona ao cardápio. As configurações usam português brasileiro e o fuso de São Paulo.
As três tabelas estão em uma migração inicial porque não havia migrações anteriores.

## Modelos e regras da aula

- `Cliente`: nome (até 100 caracteres) e telefone (texto de até 20 caracteres).
- `Produto`: nome (até 100 caracteres) e preço (`DecimalField`, 6 dígitos no total e 2 casas decimais).
- `Pedido`: cliente, produto e quantidade inteira (padrão 1). Cada pedido possui um único produto.
- `cliente` usa `CASCADE`: excluir um cliente exclui suas comandas, conforme a regra definida na aula.
- `produto` usa `PROTECT`: um produto vendido não pode ser excluído enquanto houver pedidos relacionados.

Produtos, clientes e pedidos são cadastrados pelo site, sem o Admin. Produtos também podem ser editados pelo site. A exclusão continua no Admin.
Login, vários produtos por pedido, data e total ficam para aulas posteriores, como indicado nos PDFs.

## Formulários da aula 5

No formulário de pedido, os campos `cliente` e `produto` viraram listas de escolha porque são `ForeignKey`: o pedido aponta para uma ficha que já existe, então o Django só oferece os clientes e produtos cadastrados.
Por enquanto, qualquer pessoa que souber o endereço consegue cadastrar. O login fica para o Sábado 6.

## Visual da aula 4

As cores são vermelho `#C0392B` e creme `#FFF8EE`, seguindo a aula: destacam o menu e os preços e dão um fundo acolhedor à lanchonete.
O `base.html` concentra o HTML comum, o menu e o carregamento do CSS com `{% load static %}` e `{% static %}`.
As três páginas herdam esse arquivo e preenchem `block conteudo`. Um bloco `titulo` preserva os títulos individuais das abas que já existiam.
O CSS centraliza o conteúdo e aplica cartões brancos, preços vermelhos, quantidade em destaque e sublinhado nos links ao passar o mouse ou focar pelo teclado.
Para conferir, reinicie o servidor e atualize o navegador com `Ctrl+F5`.

## Executar no PowerShell

Na pasta que contém `manage.py`, use a venv existente:

```powershell
.\venv\Scripts\python.exe manage.py migrate
.\venv\Scripts\python.exe manage.py carregar_exemplos
.\venv\Scripts\python.exe manage.py createsuperuser
.\venv\Scripts\python.exe manage.py runserver
```

Escolha seu usuário e sua senha no comando `createsuperuser`. Nenhuma conta administrativa ou senha padrão é criada automaticamente.
O comando `carregar_exemplos` pode ser repetido: adiciona os três clientes e produtos dos slides e três pedidos de demonstração sem apagar registros existentes.

- Cardápio: http://127.0.0.1:8000/cardapio/
- Clientes: http://127.0.0.1:8000/clientes/
- Pedidos: http://127.0.0.1:8000/pedidos/
- Novo produto: http://127.0.0.1:8000/produtos/novo/
- Novo pedido: http://127.0.0.1:8000/pedidos/novo/
- Novo cliente: http://127.0.0.1:8000/clientes/novo/
- Administração: http://127.0.0.1:8000/admin/

Para preparar outra máquina, crie a venv e instale as dependências antes dos comandos acima:

```powershell
py -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Verificação

```powershell
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py test
```

Os testes cobrem páginas, navegação, listas vazias, formulários (cadastro, validação e edição), cadastro no Admin, regras de exclusão e carga repetida de exemplos. Usam um banco de testes separado.

O projeto está configurado para estudo local, com `DEBUG=True`. O código está publicado em https://github.com/cleytonhercilio/pedidao.
