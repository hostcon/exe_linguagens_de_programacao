# Sistema PDV — PySide6 + SQLite

Sistema de Ponto de Venda (PDV) desktop, com interface gráfica em **PySide6** e
banco de dados **SQLite**. Feito para uso real ou como material didático
(estrutura simples, comentada e fácil de expandir em sala de aula).

## Funcionalidades

- **Aba PDV (Venda)**
  - Busca de produto por nome ou código de barras
  - Leitura por leitor de código de barras: se o código digitado bater
    exatamente com um produto cadastrado, ele já é adicionado ao carrinho
  - Carrinho com cálculo automático de subtotal e total
  - Escolha da forma de pagamento (Dinheiro, Débito, Crédito, Pix)
  - Ao finalizar a venda, o estoque dos produtos é baixado automaticamente

- **Aba Produtos**
  - Cadastro, edição e exclusão de produtos (CRUD completo)
  - Campos: nome, código de barras, categoria, preço e estoque
  - Busca/filtro em tempo real

- **Aba Histórico**
  - Lista de vendas realizadas, com filtro por período (data início/fim)
  - Total vendido no dia
  - Duplo clique numa venda abre o detalhe dos itens vendidos

## Estrutura dos arquivos

```
pdv_pyside6/
├── main.py            # Interface gráfica (janela principal e as 3 abas)
├── database.py         # Camada de acesso ao banco SQLite (classe Database)
├── seed_dados.py        # Script opcional para popular o banco com produtos de exemplo
├── requirements.txt      # Dependências do projeto
└── pdv.db              # Banco de dados SQLite (criado automaticamente na 1ª execução)
```

## Banco de dados

O SQLite é criado automaticamente (arquivo `pdv.db`) na primeira execução,
com três tabelas:

- **produtos** — id, codigo_barras, nome, categoria, preco, estoque
- **vendas** — id, data_hora, total, forma_pagamento
- **itens_venda** — id, venda_id, produto_id, nome_produto, quantidade,
  preco_unitario, subtotal (ligada a `vendas` com `ON DELETE CASCADE`)

Toda a lógica de acesso ao banco fica isolada na classe `Database`
(`database.py`), separada da interface gráfica — facilita tanto manutenção
quanto uso em sala de aula (dá pra explicar a camada de dados isoladamente).

## Como rodar

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

2. (Opcional) Popule o banco com produtos de exemplo:
   ```bash
   python seed_dados.py
   ```

3. Execute o sistema:
   ```bash
   python main.py
   ```

## Possíveis evoluções (ideias para próximas aulas)

- Emissão de recibo/cupom em PDF ao finalizar a venda
- Autenticação de operador (login/senha) e relatório por operador
- Relatório de produtos mais vendidos / gráficos (ex: com matplotlib)
- Alerta visual de estoque baixo na aba de Produtos
- Migrar `database.py` para usar um ORM (ex: SQLAlchemy) como exercício
  de comparação com SQL puro
- Exportar histórico de vendas para Excel (reaproveitando lógica parecida
  com a que você já usa nos seus projetos com openpyxl)

## Observação sobre a interface

O PySide6 é usado com `QTabWidget` para separar as três telas e
`QTableWidget` para as listagens — segue a mesma lógica de
sinais/slots (`clicked.connect`, `doubleClicked.connect`,
`returnPressed.connect`) que você já usa na apostila de PySide6, então dá
pra reaproveitar bastante conteúdo se for usar isso com os alunos.
