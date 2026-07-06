import sqlite3
import pandas as pd
from datetime import datetime

def init_db():
    conn = sqlite3.connect('tickets.db')
    
    # Tabla de tickets
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            descripcion TEXT,
            categoria TEXT,
            prioridad TEXT,
            confianza REAL,
            fecha TEXT,
            estado TEXT DEFAULT 'Pendiente',
            tiene_evidencia INTEGER DEFAULT 0,
            atendido_por_ti TEXT DEFAULT 'No'
        )
    ''')
    
    # Tabla de usuarios
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            nombre TEXT,
            rol TEXT
        )
    ''')
    
    # Usuarios por defecto
    usuarios = [
        ('admin', 'admin123', 'Administrador TI', 'ti'),
        ('jefe', 'jefe123', 'Jefe de Área', 'jefe'),
        ('usuario', 'usuario123', 'Usuario Común', 'usuario')
    ]
    
    for u in usuarios:
        conn.execute("INSERT OR IGNORE INTO users (username, password, nombre, rol) VALUES (?, ?, ?, ?)", u)
    
    conn.commit()
    conn.close()

def guardar_ticket(titulo, descripcion, categoria, prioridad, confianza, tiene_evidencia=0):
    conn = sqlite3.connect('tickets.db')
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute('''
        INSERT INTO tickets (titulo, descripcion, categoria, prioridad, confianza, fecha, tiene_evidencia)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (titulo, descripcion, categoria, prioridad, confianza, fecha, tiene_evidencia))
    conn.commit()
    conn.close()

def obtener_tickets():
    conn = sqlite3.connect('tickets.db')
    df = pd.read_sql_query("SELECT * FROM tickets ORDER BY fecha DESC", conn)
    conn.close()
    return df
def actualizar_ticket(ticket_id, estado, atendido_por_ti="Sí", respuesta=""):
    conn = sqlite3.connect('tickets.db')
    conn.execute('''
        UPDATE tickets 
        SET estado = ?, atendido_por_ti = ?, respuesta = ?
        WHERE id = ?
    ''', (estado, atendido_por_ti, respuesta, ticket_id))
    conn.commit()
    conn.close()