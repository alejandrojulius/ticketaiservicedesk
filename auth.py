import streamlit as st
import sqlite3

def login():
    st.sidebar.title("🔐 Iniciar Sesión")
    username = st.sidebar.text_input("Usuario")
    password = st.sidebar.text_input("Contraseña", type="password")
    
    if st.sidebar.button("Ingresar"):
        conn = sqlite3.connect('tickets.db')
        user = conn.execute("SELECT * FROM users WHERE username = ? AND password = ?", 
                          (username, password)).fetchone()
        conn.close()
        
        if user:
            st.session_state['logged_in'] = True
            st.session_state['username'] = user[1]
            st.session_state['nombre'] = user[3]
            st.session_state['rol'] = user[4]
            return True
        else:
            st.sidebar.error("Usuario o contraseña incorrectos")
            return False
    return False

def logout():
    if st.sidebar.button("Cerrar Sesión"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()