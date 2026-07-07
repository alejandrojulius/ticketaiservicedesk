import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

from model import clasificar_ticket
from database import init_db, guardar_ticket, obtener_tickets, actualizar_ticket
from auth import login, logout

st.set_page_config(page_title="TicketAI", layout="wide")
st.title("🧠 TicketAI - Sistema Inteligente de Service Desk")

init_db()

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    login()
    st.stop()

st.sidebar.success(f"👤 {st.session_state['nombre']}")
st.sidebar.info(f"Rol: {st.session_state['rol'].upper()}")
logout()

# Menú principal con tabs
tab1, tab2, tab3, tab4 = st.tabs(["Nuevo Ticket", "Dashboard", "Gestionar Tickets", "Historial"])

with tab1:  # Nuevo Ticket
    st.subheader("📋 Ingresar Nuevo Ticket")
    tipo_ticket = st.selectbox("Tipo de Ticket *", ["Incidente", "Requerimiento"])
    titulo = st.text_input("Título del ticket *")
    descripcion = st.text_area("Descripción del problema *", height=150)
    archivo = st.file_uploader("Adjuntar evidencia", type=["jpg", "jpeg", "png", "docx", "pdf"])
    
    if st.button("🔍 Clasificar y Registrar Ticket", type="primary"):
        if titulo and descripcion:
            with st.spinner("Analizando con IA..."):
                resultado = clasificar_ticket(titulo, descripcion)
            
            if tipo_ticket == "Incidente":
                resultado["prioridad"] = "Alta"
            else:
                resultado["prioridad"] = "Media"
            
            tiene_evidencia = 1 if archivo is not None else 0
            ticket_id = guardar_ticket(tipo_ticket, titulo, descripcion, resultado["categoria"], resultado["prioridad"], resultado["confianza"], tiene_evidencia)
            
            st.success(f"✅ Ticket registrado - **ID: {ticket_id}**")
            
            if archivo is not None:
                os.makedirs("uploads", exist_ok=True)
                with open(f"uploads/{archivo.name}", "wb") as f:
                    f.write(archivo.getbuffer())
                st.success(f"📎 Evidencia adjuntada: {archivo.name}")
        else:
            st.error("Completa título y descripción")

with tab2:  # Dashboard
    st.subheader("📊 Dashboard")
    df = obtener_tickets()
    if not df.empty:
        if st.session_state['rol'] == 'ti':
            col1, col2, col3 = st.columns(3)
            with col1: st.metric("Total", len(df))
            with col2: st.metric("Pendientes", len(df[df['estado']=='Pendiente']))
            with col3: st.metric("Resueltos", len(df[df['estado']=='Resuelto']))
            
            col4, col5 = st.columns(2)
            with col4:
                fig = px.bar(df['categoria'].value_counts(), title="Tickets por Categoría")
                st.plotly_chart(fig, use_container_width=True)
            with col5:
                fig2 = px.pie(df, names='estado', title="Estado de Tickets")
                st.plotly_chart(fig2, use_container_width=True)
            
            st.dataframe(df, use_container_width=True)
        else:
            st.dataframe(df, use_container_width=True)
    else:
        st.info("No hay tickets.")

with tab3:  # Gestionar Tickets (Solo TI)
    if st.session_state['rol'] == 'ti':
        st.subheader("🔧 Gestionar Tickets")
        df = obtener_tickets()
        for index, row in df.iterrows():
            with st.expander(f"{row['id']} - {row['titulo']}"):
                st.write(f"**Descripción:** {row['descripcion']}")
                nuevo_estado = st.selectbox("Estado", ["Pendiente", "En Espera", "Atendido", "Reasignado"], key=f"est_{row['id']}")
                respuesta = st.text_area("Respuesta al usuario", key=f"resp_{row['id']}")
                if st.button("Guardar Cambios", key=f"btn_{row['id']}"):
                    actualizar_ticket(row['id'], nuevo_estado, "Sí", respuesta)
                    st.success("Ticket actualizado")
                    st.rerun()

with tab4:  # Historial
    st.subheader("📜 Historial de Tickets")
    df = obtener_tickets()
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No hay tickets registrados.")

st.caption("Proyecto de Titulación - Cibertec | TicketAI con IA")