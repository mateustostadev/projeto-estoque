from models import Usuario, Produto, MovimentacaoEstoque, RelatorioEstoque, SolicitacaoCompra

# Criar usuários para testes
estoquista = Usuario(nome="João", cargo="estoquista")
usuario = Usuario(nome="Maria", cargo="usuario")
gerente = Usuario(nome="Carlos", cargo="gerente")

# Teste de cadastro de produtos
Produto.cadastrar(estoquista, nome="Teclado", categoria_id=1, quantidade=10, preco=150.0, localizacao="A1")
Produto.cadastrar(estoquista, nome="Mouse", categoria_id=1, quantidade=5, preco=80.0, localizacao="A2")

# Teste de consulta de localização de produto
Produto.consultar_localizacao(produto_id=1)

# Teste de movimentação de entrada no estoque
MovimentacaoEstoque.registrar_entrada(estoquista, produto_id=1, quantidade=5, nota_fiscal="NF12345")

# Teste de movimentação de saída no estoque
MovimentacaoEstoque.registrar_saida(estoquista, produto_id=1, quantidade=3)

# Teste de relatório de produtos com estoque baixo
RelatorioEstoque.produtos_com_estoque_baixo(usuario, limite_minimo=5)

# Teste de relatório de movimentação de produtos em um período
data_inicial = "2024-01-01"
data_final = "2024-12-31"
RelatorioEstoque.movimentacao_produtos(usuario, data_inicial, data_final)

# Teste de solicitação de compra
SolicitacaoCompra.solicitar_compra(usuario, produto_id=1, quantidade=20)

# Teste de autorização de solicitação de compra
SolicitacaoCompra.autorizar_compra(gerente, solicitacao_id=1)
