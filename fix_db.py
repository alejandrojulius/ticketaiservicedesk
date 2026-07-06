import sqlite3

conn = sqlite3.connect('tickets.db')

# Agregar columnas faltantes
try:
    conn.execute("ALTER TABLE tickets ADD COLUMN estado TEXT DEFAULT 'Pendiente'")
except:
    pass

try:
    conn.execute("ALTER TABLE tickets ADD COLUMN tiene_evidencia INTEGER DEFAULT 0")
except:
    pass

try:
    conn.execute("ALTER TABLE tickets ADD COLUMN atendido_por_ti TEXT DEFAULT 'No'")
except:
    pass

try:
    conn.execute("ALTER TABLE tickets ADD COLUMN respuesta TEXT")
except:
    pass

conn.commit()
conn.close()
print("✅ Columnas agregadas correctamente. Tus datos se conservaron.")