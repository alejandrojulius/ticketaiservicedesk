import sqlite3
import pandas as pd
from datetime import datetime

def init_db():
    conn = sqlite3.connect('tickets.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            descripcion TEXT,
            categoria TEXT,
            prioridad TEXT,
            confianza REAL,
            fecha TEXT,
            estado TEXT DEFAULT 'Pendiente'
        )
    ''')
    conn.close()

def guardar_ticket(titulo, descripcion, categoria, prioridad, confianza):
    conn = sqlite3.connect('tickets.db')
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute('''
        INSERT INTO tickets (titulo, descripcion, categoria, prioridad, confianza, fecha)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (titulo, descripcion, categoria, prioridad, confianza, fecha))
    conn.commit()
    conn.close()

def obtener_tickets():
    conn = sqlite3.connect('tickets.db')
    df = pd.read_sql_query("SELECT * FROM tickets ORDER BY fecha DESC", conn)
    conn.close()
    return df