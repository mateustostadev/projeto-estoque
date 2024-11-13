from models import Produto, MovimentacaoEstoque

# Teste de entrada e saída de produtos
MovimentacaoEstoque.registrar_entrada(produto_id=1, quantidade=5)


# Teste de rastreamento de localização
Produto.consultar_localizacao(produto_id=1)
