import sqlite3
import pandas as pd

def conectar():
    return sqlite3.connect('financas.db')


# ÁREA DAS TRANSAÇÕES PRINCIPAIS

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,         -- NOVA COLUNA: Dono do registro
            tipo TEXT NOT NULL,            -- 'Receita' ou 'Despesa'
            categoria TEXT NOT NULL,
            descricao TEXT,
            valor REAL NOT NULL,
            data DATE NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def inserir_transacao(usuario, tipo, categoria, descricao, valor, data):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transacoes (usuario, tipo, categoria, descricao, valor, data) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (usuario, tipo, categoria, descricao, valor, data))
    conn.commit()
    conn.close()

def buscar_transacoes(usuario):
    conn = conectar()
    # Separação de informação por usuário
    df = pd.read_sql_query("SELECT * FROM transacoes WHERE usuario = ?", conn, params=(usuario,))
    conn.close()
    return df

def excluir_transacao(id_transacao, usuario):
    conn = conectar()
    cursor = conn.cursor()
    # SEGURANÇA
    cursor.execute('''
        DELETE FROM transacoes WHERE id = ? AND usuario = ?
    ''', (id_transacao, usuario))
    conn.commit()
    conn.close()


# ÁREA DOS LEMBRETES

def criar_tabela_lembretes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lembretes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,         -- NOVA COLUNA: Dono do lembrete
            titulo TEXT NOT NULL,
            valor REAL NOT NULL,
            data_vencimento DATE NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def inserir_lembrete(usuario, titulo, valor, data):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO lembretes (usuario, titulo, valor, data_vencimento) 
        VALUES (?, ?, ?, ?)
    ''', (usuario, titulo, valor, data))
    conn.commit()
    conn.close()

def buscar_lembretes(usuario):
    conn = conectar()
    # Filtra por usuário e já entrega ordenado pela data
    df = pd.read_sql_query("SELECT * FROM lembretes WHERE usuario = ? ORDER BY data_vencimento ASC", conn, params=(usuario,))
    conn.close()
    return df

def excluir_lembrete(id_lembrete, usuario):
    conn = conectar()
    cursor = conn.cursor()
    # SEGURANÇA
    cursor.execute('DELETE FROM lembretes WHERE id = ? AND usuario = ?', (id_lembrete, usuario))
    conn.commit()
    conn.close()

# ÁREA DAS METAS DE ORÇAMENTO

def criar_tabela_metas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS metas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            categoria TEXT NOT NULL,
            limite REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def definir_meta(usuario, categoria, limite):
    conn = conectar()
    cursor = conn.cursor()
    # Lógica Inteligente: Verifica se a pessoa já tem uma meta para essa categoria
    cursor.execute("SELECT id FROM metas WHERE usuario=? AND categoria=?", (usuario, categoria))
    existe = cursor.fetchone()
    
    if existe:
        # Se já existe, apenas atualiza o valor novo (UPDATE)
        cursor.execute("UPDATE metas SET limite=? WHERE id=?", (limite, existe[0]))
    else:
        # Se não existe, cria do zero (INSERT)
        cursor.execute("INSERT INTO metas (usuario, categoria, limite) VALUES (?, ?, ?)", (usuario, categoria, limite))
    conn.commit()
    conn.close()

def buscar_metas(usuario):
    conn = conectar()
    df = pd.read_sql_query("SELECT * FROM metas WHERE usuario = ?", conn, params=(usuario,))
    conn.close()
    return df