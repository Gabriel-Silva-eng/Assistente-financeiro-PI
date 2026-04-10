import sqlite3
import pandas as pd

def conectar():
    return sqlite3.connect('financas.db')

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,         -- 'Receita' ou 'Despesa'
            categoria TEXT NOT NULL,    -- Ex: 'Alimentação', 'Salário'
            descricao TEXT,             -- Detalhes do gasto/ganho
            valor REAL NOT NULL,        -- O valor em si
            data DATE NOT NULL          -- Quando ocorreu
        )
    ''')
    conn.commit()
    conn.close()

def inserir_transacao(tipo, categoria, descricao, valor, data):
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO transacoes (tipo, categoria, descricao, valor, data)
        VALUES (?, ?, ?, ?, ?)
    ''', (tipo, categoria, descricao, valor, data))
    
    conn.commit()
    conn.close()

def buscar_transacoes():
    conn = conectar()
    df = pd.read_sql_query("SELECT * FROM transacoes", conn)
    conn.close()
    return df

def excluir_transacao(id_transacao):
    conn = conectar()
    cursor = conn.cursor()
    

    cursor.execute('''
        DELETE FROM transacoes WHERE id = ?
    ''', (id_transacao,))
    
    conn.commit()
    conn.close()

    
def criar_tabela_lembretes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lembretes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            valor REAL NOT NULL,
            data_vencimento DATE NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def inserir_lembrete(titulo, valor, data):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO lembretes (titulo, valor, data_vencimento) VALUES (?, ?, ?)', (titulo, valor, data))
    conn.commit()
    conn.close()

def buscar_lembretes():
    import pandas as pd
    conn = conectar()
    df = pd.read_sql_query("SELECT * FROM lembretes ORDER BY data_vencimento ASC", conn)
    conn.close()
    return df

def excluir_lembrete(id_lembrete):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM lembretes WHERE id = ?', (id_lembrete,))
    conn.commit()
    conn.close()