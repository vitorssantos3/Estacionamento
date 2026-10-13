import sqlite3
from datetime import datetime

DB_NAME = 'estacionamento.db'

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row 
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS veiculos_patio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            placa TEXT NOT NULL,
            data_entrada TEXT NOT NULL,
            data_saida TEXT,
            status TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def registrar_entrada_veiculo(placa_veiculo):
    conn = get_connection()
    cursor = conn.cursor()
    
    data_hora_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    sql_insert = """
        INSERT INTO veiculos_patio (placa, data_entrada, status)
        VALUES (?, ?, ?)
    """
    
    cursor.execute(sql_insert, (placa_veiculo, data_hora_atual, 'ATIVO'))
    conn.commit()
    conn.close()

def buscar_veiculos_estacionados():
    conn = get_connection()
    cursor = conn.cursor()
    
    sql_select = "SELECT id, placa, data_entrada, status FROM veiculos_patio WHERE status = 'ATIVO'"
    cursor.execute(sql_select)
    linhas = cursor.fetchall()
    
    conn.close()
    return linhas

def verificar_placa_ja_estacionada(placa_veiculo):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM veiculos_patio WHERE placa = ? AND status = 'ATIVO'", (placa_veiculo,))
    resultado = cursor.fetchone()
    conn.close()
    
    return resultado is not None

def buscar_veiculo_por_placa(placa_veiculo):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, placa, data_entrada, status FROM veiculos_patio WHERE placa = ? AND status = 'ATIVO'", (placa_veiculo,))
    resultado = cursor.fetchone()
    conn.close()
    
    return resultado