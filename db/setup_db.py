import sqlite3
import os

# Define o caminho do banco de dados
DB_PATH = os.path.join(os.path.dirname(__file__), 'estoque.db')

# Função para criar as tabelas
def criar_tabelas():
    # Conecta ao banco de dados (cria o arquivo se não existir)
    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()
    
    # Cria a tabela de produtos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            categoria_id INTEGER,
            quantidade INTEGER DEFAULT 0,
            preco REAL NOT NULL,
            localizacao TEXT,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id)
        )
    ''')
    
    # Cria a tabela de categorias
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE
        )
    ''')

    # Cria a tabela de movimentações de estoque
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER,
            data TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            tipo TEXT CHECK(tipo IN ('entrada', 'saida')) NOT NULL,
            FOREIGN KEY (produto_id) REFERENCES produtos(id)
        )
    ''')

    # Cria a tabela de tipos de usuário para permissões
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tipos_usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL UNIQUE,
            descricao TEXT NOT NULL
        )
    ''')

    # Insere os tipos de usuário padrão
    cursor.execute("INSERT OR IGNORE INTO tipos_usuario (tipo, descricao) VALUES ('estoquista', 'Permite cadastrar e movimentar produtos')")
    cursor.execute("INSERT OR IGNORE INTO tipos_usuario (tipo, descricao) VALUES ('usuario', 'Permite consultar relatórios de estoque')")
    cursor.execute("INSERT OR IGNORE INTO tipos_usuario (tipo, descricao) VALUES ('gerente', 'Permite autorizar solicitações de compra')")

    # Cria a tabela de solicitações de compra
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS solicitacoes_compra (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER NOT NULL,
            quantidade INTEGER NOT NULL,
            status TEXT CHECK(status IN ('pendente', 'autorizado', 'cancelado')) NOT NULL DEFAULT 'pendente',
            FOREIGN KEY (produto_id) REFERENCES produtos(id)
        )
    ''')

    # Confirma as mudanças e fecha a conexão
    conexao.commit()
    conexao.close()
    print("Tabelas criadas com sucesso, incluindo tipos de usuário e solicitações de compra.")

# Executa a criação das tabelas ao rodar o script
if __name__ == "__main__":
    criar_tabelas()
