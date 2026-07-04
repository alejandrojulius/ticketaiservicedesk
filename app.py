import streamlit as st
from model import clasificar_ticket
from database import init_db, guardar_ticket, obtener_tickets
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="TicketAI", layout="wide")
st.title("🧠 TicketAI - Sistema Inteligente de Service Desk")

init_db()  # Inicializar base de datos

menu = st.sidebar.selectbox("Menú", ["Nuevo Ticket", "Dashboard", "Historial"])

if menu == "Nuevo Ticket":
    st.subheader("📋 Ingresar Nuevo Ticket")
    titulo = st.text_input("Título del ticket")
    descripcion = st.text_area("Descripción del problema", height=150)
    
    if st.button("🔍 Clasificar con IA", type="primary"):
        if titulo and descripcion:
            with st.spinner("Analizando con Inteligencia Artificial..."):
                resultado = clasificar_ticket(titulo, descripcion)
            
            st.success("✅ Ticket procesado correctamente")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Categoría", resultado["categoria"])
            col2.metric("Prioridad", resultado["prioridad"])
            col3.metric("Confianza", f"{resultado['confianza']}%")
            
            st.info(f"**Explicación de la IA:** {resultado['explicacion']}")
            
            # Guardar en base de datos
            guardar_ticket(titulo, descripcion, resultado["categoria"], 
                         resultado["prioridad"], resultado["confianza"])
        else:
            st.error("Por favor completa todos los campos")

elif menu == "Dashboard":
    st.subheader("📊 Dashboard")
    df = obtener_tickets()
    
    if not df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico correcto con Plotly
            fig = px.bar(df['categoria'].value_counts(), 
                        title="Tickets por Categoría",
                        labels={'index': 'Categoría', 'value': 'Cantidad'})
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig2 = px.pie(df, names='categoria', title="Distribución por Categoría")
            st.plotly_chart(fig2, use_container_width=True)
            
            st.metric("Total de tickets procesados", len(df))
    else:
        st.info("Aún no hay tickets registrados. Crea algunos para ver el dashboard.")

elif menu == "Historial":
    st.subheader("📜 Historial de Tickets")
    df = obtener_tickets()
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No hay tickets aún.")

st.caption("Proyecto de Titulación - Cibertec | TicketAI con IA")