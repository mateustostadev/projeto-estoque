import sqlite3
import os

# Define o caminho do banco de dados
DB_PATH = os.path.join(os.path.dirname(__file__), '../db/estoque.db')

# Definir os cargos permitidos
CARGOS_PERMITIDOS = {
    "estoquista": "estoquista",
    "usuario": "usuario",
    "gerente": "gerente"
}

# Classe Usuario para gerenciar o cargo e permissões
class Usuario:
    def __init__(self, nome, cargo):
        self.nome = nome
        self.cargo = cargo

    def verificar_permissao(self, cargo_necessario):
        """Verifica se o cargo do usuário é suficiente para a operação."""
        if self.cargo != cargo_necessario:
            print(f"Acesso negado: {self.nome} (Cargo: {self.cargo}) não possui permissão para essa operação.")
            return False
        return True

# Classe Produto com permissão de cadastro
class Produto:
    def __init__(self, nome, categoria_id, quantidade, preco, localizacao):
        self.nome = nome
        self.categoria_id = categoria_id
        self.quantidade = quantidade
        self.preco = preco
        self.localizacao = localizacao

    @staticmethod
    def cadastrar(usuario, nome, categoria_id, quantidade, preco, localizacao):
        if not usuario.verificar_permissao(CARGOS_PERMITIDOS["estoquista"]):
            return

        conexao = sqlite3.connect(DB_PATH)
        cursor = conexao.cursor()
        
        # Verifica duplicação
        cursor.execute("SELECT * FROM produtos WHERE nome = ?", (nome,))
        if cursor.fetchone():
            print("Erro: Produto já cadastrado.")
            conexao.close()
            return
        
        # Cadastra o produto
        cursor.execute('''
            INSERT INTO produtos (nome, categoria_id, quantidade, preco, localizacao)
            VALUES (?, ?, ?, ?, ?)
        ''', (nome, categoria_id, quantidade, preco, localizacao))
        
        conexao.commit()
        conexao.close()
        print(f"Produto '{nome}' cadastrado com sucesso.")

    @staticmethod
    def consultar_localizacao(produto_id):
        """Consulta a localização de um produto no depósito."""
        conexao = sqlite3.connect(DB_PATH)
        cursor = conexao.cursor()
        
        cursor.execute("SELECT localizacao FROM produtos WHERE id = ?", (produto_id,))
        resultado = cursor.fetchone()
        
        conexao.close()
        if resultado:
            print(f"Localização do produto ID {produto_id}: {resultado[0]}")
        else:
            print("Produto não encontrado.")


# Classe MovimentacaoEstoque com permissão de registrar entrada e saída
class MovimentacaoEstoque:
    def __init__(self, produto_id, data, quantidade, tipo):
        self.produto_id = produto_id
        self.data = data
        self.quantidade = quantidade
        self.tipo = tipo

    @staticmethod
    def registrar_entrada(usuario, produto_id, quantidade, nota_fiscal):
        """Registra uma entrada de produto no estoque, com validação de nota fiscal."""
        if not usuario.verificar_permissao(CARGOS_PERMITIDOS["estoquista"]):
            return

        if not nota_fiscal:
            print("Erro: Nota fiscal é obrigatória para registrar a entrada de produto.")
            return

        conexao = sqlite3.connect(DB_PATH)
        cursor = conexao.cursor()
        
        # Atualizar quantidade no estoque
        cursor.execute("UPDATE produtos SET quantidade = quantidade + ? WHERE id = ?", (quantidade, produto_id))
        # Registrar a movimentação
        cursor.execute('''
            INSERT INTO movimentacoes (produto_id, data, quantidade, tipo)
            VALUES (?, date('now'), ?, 'entrada')
        ''', (produto_id, quantidade))
        
        conexao.commit()
        conexao.close()
        print(f"Entrada de {quantidade} unidades do produto ID {produto_id} registrada com sucesso.")

    @staticmethod
    def registrar_saida(usuario, produto_id, quantidade):
        """Registra uma saída de produto do estoque, reduzindo a quantidade."""
        if not usuario.verificar_permissao(CARGOS_PERMITIDOS["estoquista"]):
            return

        conexao = sqlite3.connect(DB_PATH)
        cursor = conexao.cursor()
        
        # Verificar se a quantidade atual é suficiente para saída
        cursor.execute("SELECT quantidade FROM produtos WHERE id = ?", (produto_id,))
        quantidade_atual = cursor.fetchone()
        if quantidade_atual is None or quantidade_atual[0] < quantidade:
            print("Erro: Quantidade insuficiente para saída.")
            conexao.close()
            return
        
        # Atualizar quantidade no estoque
        cursor.execute("UPDATE produtos SET quantidade = quantidade - ? WHERE id = ?", (quantidade, produto_id))
        # Registrar a movimentação
        cursor.execute('''
            INSERT INTO movimentacoes (produto_id, data, quantidade, tipo)
            VALUES (?, date('now'), ?, 'saida')
        ''', (produto_id, quantidade))
        
        conexao.commit()
        conexao.close()
        print(f"Saída de {quantidade} unidades do produto ID {produto_id} registrada com sucesso.")


class RelatorioEstoque:
    @staticmethod
    def produtos_com_estoque_baixo(usuario, limite_minimo=10):
        if not usuario.verificar_permissao(CARGOS_PERMITIDOS["usuario"]):
            return

        conexao = sqlite3.connect(DB_PATH)
        cursor = conexao.cursor()
        cursor.execute("SELECT nome, quantidade FROM produtos WHERE quantidade < ?", (limite_minimo,))
        produtos_baixo_estoque = cursor.fetchall()
        conexao.close()
        
        print("Produtos com estoque baixo:")
        for produto in produtos_baixo_estoque:
            print(f"Produto: {produto[0]}, Quantidade: {produto[1]}")
    
    @staticmethod
    def movimentacao_produtos(usuario, data_inicial, data_final):
        if not usuario.verificar_permissao(CARGOS_PERMITIDOS["usuario"]):
            return

        conexao = sqlite3.connect(DB_PATH)
        cursor = conexao.cursor()
        cursor.execute(
            '''
            SELECT produto_id, tipo, quantidade, data
            FROM movimentacoes
            WHERE data BETWEEN ? AND ?
            ''',
            (data_inicial, data_final)
        )
        movimentacoes = cursor.fetchall()
        conexao.close()
        
        print("Movimentação de produtos:")
        for movimentacao in movimentacoes:
            print(f"Produto: {movimentacao[0]}, Tipo: {movimentacao[1]}, Quantidade: {movimentacao[2]}, Data: {movimentacao[3]}")


# Classe SolicitacaoCompra para lidar com as solicitações de compra com controle de permissão
class SolicitacaoCompra:
    @staticmethod
    def solicitar_compra(usuario, produto_id, quantidade):
        if not usuario.verificar_permissao(CARGOS_PERMITIDOS["usuario"]):
            return

        conexao = sqlite3.connect(DB_PATH)
        cursor = conexao.cursor()

        # Inserir a solicitação na tabela
        cursor.execute("""
            INSERT INTO solicitacoes_compra (produto_id, quantidade, status)
            VALUES (?, ?, 'pendente')
        """, (produto_id, quantidade))

        conexao.commit()
        conexao.close()
        print(f"Solicitação de compra de {quantidade} unidades do produto ID {produto_id} registrada com sucesso.")

    @staticmethod
    def autorizar_compra(usuario, solicitacao_id):
        if not usuario.verificar_permissao(CARGOS_PERMITIDOS["gerente"]):
            return

        conexao = sqlite3.connect(DB_PATH)
        cursor = conexao.cursor()

        # Verificar se a solicitação existe e está pendente
        cursor.execute("SELECT status FROM solicitacoes_compra WHERE id = ?", (solicitacao_id,))
        resultado = cursor.fetchone()
        if not resultado:
            print("Erro: Solicitação de compra não encontrada.")
            conexao.close()
            return
        elif resultado[0] != 'pendente':
            print("Erro: Solicitação de compra já foi autorizada ou cancelada.")
            conexao.close()
            return

        # Atualizar o status para 'autorizado'
        cursor.execute("UPDATE solicitacoes_compra SET status = 'autorizado' WHERE id = ?", (solicitacao_id,))
        conexao.commit()
        conexao.close()
        print(f"Solicitação de compra ID {solicitacao_id} autorizada com sucesso.")
