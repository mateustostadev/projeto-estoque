# Documentação do Sistema de Gerenciamento de Estoque

## 1. Definição de Estruturas de Dados

O sistema é composto por várias tabelas e classes que organizam os dados principais para o gerenciamento de estoque.

### Estruturas de Dados do Banco de Dados (`setup_db.py`)

1. **Tabela `produtos`**: Armazena os produtos do estoque.
   - **Colunas**:
     - `id`: Identificador único do produto.
     - `nome`: Nome do produto (texto único).
     - `categoria_id`: Referência à categoria do produto.
     - `quantidade`: Quantidade em estoque.
     - `preco`: Preço unitário.
     - `localizacao`: Localização no depósito.

2. **Tabela `categorias`**: Organiza os produtos em categorias.
   - **Colunas**:
     - `id`: Identificador único da categoria.
     - `nome`: Nome único da categoria.

3. **Tabela `movimentacoes`**: Registra as movimentações de entrada e saída de produtos no estoque.
   - **Colunas**:
     - `id`: Identificador único da movimentação.
     - `produto_id`: Referência ao produto.
     - `data`: Data da movimentação.
     - `quantidade`: Quantidade movimentada.
     - `tipo`: Tipo de movimentação (`entrada` ou `saida`).

4. **Tabela `tipos_usuario`**: Controla os diferentes níveis de acesso ao sistema.
   - **Colunas**:
     - `id`: Identificador único do tipo de usuário.
     - `tipo`: Tipo de usuário (e.g., estoquista, usuário, gerente).
     - `descricao`: Descrição das permissões do tipo de usuário.

5. **Tabela `solicitacoes_compra`**: Registra as solicitações de compra realizadas no sistema.
   - **Colunas**:
     - `id`: Identificador único da solicitação.
     - `produto_id`: ID do produto solicitado.
     - `quantidade`: Quantidade solicitada.
     - `status`: Estado da solicitação (`pendente`, `autorizado`, `cancelado`).

### Estruturas de Dados no Código (`models.py`)

1. **Produto**: Classe que representa os produtos cadastrados no sistema.
   - **Atributos**: `nome`, `categoria_id`, `quantidade`, `preco`, `localizacao`.

2. **Usuario**: Classe que define as permissões de cada usuário no sistema.
   - **Atributos**: `nome`, `cargo`.

3. **MovimentacaoEstoque**: Classe que lida com movimentações de entrada e saída de produtos.
   - **Atributos**: `produto_id`, `data`, `quantidade`, `tipo`.

4. **RelatorioEstoque**: Classe que gera relatórios sobre o estoque e movimentações.
5. **SolicitacaoCompra**: Classe que lida com a solicitação e autorização de compras.

## 2. Algoritmos de Cadastro e Consulta

### Cadastro de Produtos (`models.py`)
O método `Produto.cadastrar()` permite cadastrar novos produtos no sistema, verificando a duplicidade e exigindo permissão.

**Função**: `Produto.cadastrar(usuario, nome, categoria_id, quantidade, preco, localizacao)`
- **Parâmetros**: `usuario`, `nome`, `categoria_id`, `quantidade`, `preco`, `localizacao`.
- **Saída**: Mensagem de sucesso ou erro.

### Consulta de Localização de Produto (`models.py`)
O método `Produto.consultar_localizacao()` permite verificar a localização de um produto no depósito.

**Função**: `Produto.consultar_localizacao(produto_id)`
- **Parâmetro**: `produto_id`.
- **Saída**: Localização do produto ou mensagem de erro.

## 3. Algoritmos de Movimentação

### Registro de Entrada no Estoque (`models.py`)
O método `MovimentacaoEstoque.registrar_entrada()` registra uma entrada de produtos no estoque e exige uma nota fiscal.

**Função**: `MovimentacaoEstoque.registrar_entrada(usuario, produto_id, quantidade, nota_fiscal)`
- **Parâmetros**: `usuario`, `produto_id`, `quantidade`, `nota_fiscal`.
- **Saída**: Mensagem de sucesso ou erro.

### Registro de Saída do Estoque (`models.py`)
O método `MovimentacaoEstoque.registrar_saida()` registra uma saída de produtos do estoque.

**Função**: `MovimentacaoEstoque.registrar_saida(usuario, produto_id, quantidade)`
- **Parâmetros**: `usuario`, `produto_id`, `quantidade`.
- **Saída**: Mensagem de sucesso ou erro, com verificação de quantidade suficiente.

## 4. Relatórios e Consultas

### Relatório de Produtos com Estoque Baixo (`models.py`)
O método `RelatorioEstoque.produtos_com_estoque_baixo()` exibe produtos com quantidade abaixo de um limite mínimo.

**Função**: `RelatorioEstoque.produtos_com_estoque_baixo(usuario, limite_minimo=10)`
- **Parâmetros**: `usuario`, `limite_minimo`.
- **Saída**: Lista de produtos com baixo estoque.

### Relatório de Movimentação por Período (`models.py`)
O método `RelatorioEstoque.movimentacao_produtos()` exibe movimentações em um intervalo de datas.

**Função**: `RelatorioEstoque.movimentacao_produtos(usuario, data_inicial, data_final)`
- **Parâmetros**: `usuario`, `data_inicial`, `data_final`.
- **Saída**: Lista de movimentações realizadas no intervalo fornecido.

### Relatório de Solicitações de Compra (`models.py`)
A classe `SolicitacaoCompra` possui métodos para solicitar e autorizar compras.

- **Solicitar Compra**: `SolicitacaoCompra.solicitar_compra(usuario, produto_id, quantidade)`
- **Autorizar Compra**: `SolicitacaoCompra.autorizar_compra(usuario, solicitacao_id)`

## 5. Função de Criação de Tabelas (`setup_db.py`)

O arquivo `setup_db.py` possui a função `criar_tabelas()`, que cria todas as tabelas do sistema.

**Função**: `criar_tabelas()`
- **Processo**: 
  - Cria as tabelas `produtos`, `categorias`, `movimentacoes`, `tipos_usuario`, e `solicitacoes_compra`.
  - Preenche a tabela `tipos_usuario` com valores padrão para "estoquista", "usuario" e "gerente".
- **Execução**: A função é executada automaticamente quando o script é rodado diretamente.

---

