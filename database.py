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
    
    # ATENÇÃO: O comando DELETE sem a cláusula WHERE apaga o banco inteiro.
    # O WHERE id = ? garante que apenas uma linha sofra as consequências.
    cursor.execute('''
        DELETE FROM transacoes WHERE id = ?
    ''', (id_transacao,))
    
    conn.commit()
    conn.close()