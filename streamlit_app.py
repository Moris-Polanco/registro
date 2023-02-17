import streamlit as st
import sqlite3

# Conexión a la base de datos
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Creación de la tabla de usuarios si no existe
c.execute('''CREATE TABLE IF NOT EXISTS users
             (name TEXT, email TEXT, password TEXT)''')

# Título de la página
st.title("Registro / Inicio de Sesión")

# Página de registro
if st.button("Registrarse"):
    st.subheader("Registro")
    # Formulario de registro
    name = st.text_input("Nombre completo")
    email = st.text_input("Correo electrónico")
    password = st.text_input("Contraseña", type="password")
    confirm_password = st.text_input("Confirmar contraseña", type="password")
    
    # Botón de registro
    if st.button("Registrarse", key="register_button"):
        # Validación de contraseña
        if password == confirm_password:
            # Insertar los datos del usuario en la base de datos
            c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
            conn.commit()
            # Mensaje de confirmación
            st.success("Te has registrado correctamente")
        else:
            # Mensaje de error
            st.error("Las contraseñas no coinciden")
            
# Página de inicio de sesión
if st.button("Iniciar Sesión", key="login_button"):
    st.subheader("Inicio de Sesión")
    # Formulario de inicio de sesión
    email = st.text_input("Correo electrónico")
    password = st.text_input("Contraseña", type="password")
    
    # Botón de inicio de sesión
    if st.button("Iniciar Sesión"):
        # Buscar el usuario en la base de datos
        query = "SELECT * FROM users WHERE email=? AND password=?"
        result = c.execute(query, (email, password))
        user = result.fetchone()
        
        # Validar el inicio de sesión
        if user is not None:
            # Mensaje de confirmación
            st.success("Inicio de sesión exitoso")
            # Redireccionamiento a la página de evaluador de ensayos
            st.markdown(f"Redireccionando a https://evaluador-ensayos.streamlit.app")
            st.experimental_rerun()
        else:
            # Mensaje de error
            st.error("Credenciales incorrectas")

# Cerrar la conexión con la base de datos
conn.close()
