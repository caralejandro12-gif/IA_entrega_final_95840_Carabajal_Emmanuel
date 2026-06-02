import os
import streamlit as st
import pandas as pd
from utils.api_handler import generar_catalogo_ia
from utils.storage import guardar_consulta, obtener_historial, eliminar_consulta
from datetime import datetime
from PIL import Image

# Configuración de la página
st.set_page_config(page_title="Artelanitas Global AI", layout="wide")

# Inicialización Agéntica: Menú lateral navegable
st.sidebar.title("Menú de Navegación")
pagina = st.sidebar.radio("Ir a:", ["Inicio (Cómo funciona)", "Generador de Catálogo", "Análisis e Historial"])

if pagina == "Inicio (Cómo funciona)":
    st.title("🧶 Artelanitas Global E-commerce AI")
    st.markdown("""
    ### Descripción
    Bienvenido al asistente de internacionalización de Artelanitas. Esta herramienta utiliza Inteligencia Artificial para transformar las características básicas de tus tejidos artesanales en publicaciones de venta optimizadas para mercados globales.
    
    ### ¿Cómo funciona?
    1. Ve a la pestaña **Generador de Catálogo**.
    2. Ingresa los datos técnicos de la prenda (tipo, material, color, talle local).
    3. Selecciona el mercado/país objetivo.
    4. Haz clic en el botón de generación. La IA redactará el SEO, el storytelling y la conversión de talles.
    5. Los resultados se guardarán automáticamente para futuras consultas en la pestaña **Análisis e Historial**.
    """)

elif pagina == "Generador de Catálogo":
    st.header("✨ Generador de Publicaciones Inteligente")
    
    # Maquetado de formulario limpio
    with st.form("form_generador"):
        col1, col2 = st.columns(2)
        with col1:
            prenda = st.text_input("Tipo de Prenda", placeholder="Ej: Suéter de cuello alto")
            material = st.text_input("Material Principal", placeholder="Ej: Lana Merino 100%")
            talle = st.text_input("Talle (Argentina)", placeholder="Ej: 42 o M")
        with col2:
            color = st.text_input("Color/Acabado", placeholder="Ej: Verde esmeralda jaspeado")
            pais = st.selectbox("Mercado de Destino", ["Estados Unidos", "Reino Unido", "España", "Brasil", "Francia"])
            imagen_catalogo = st.file_uploader("Sube una foto del tejido", type=["jpg", "png", "jpeg"])
            
        submit = st.form_submit_button("Generar Catálogo con IA")
        
    if submit:
        if prenda and material and talle and color:
            with st.spinner("La IA está redactando tu publicación y analizando la foto..."):
                imagen_pil = Image.open(imagen_catalogo) if imagen_catalogo else None
                resultado_ia = generar_catalogo_ia(prenda, material, color, talle, pais, imagen=imagen_pil)
                
            # Persistencia de Datos Local (se ejecuta siempre después de las generaciones)
            datos_guardar = {
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "prenda": prenda,
                "material": material,
                "color": color,
                "talle": talle,
                "mercado": pais,
                "estado": "Generado",
                "resultado": resultado_ia
            }
            guardar_consulta(datos_guardar)
            
            # Mostrar resultados en pantalla
            st.success("¡Publicación generada con éxito!")
            st.markdown("---")
            st.markdown(resultado_ia)
        else:
            st.warning("Por favor, completa todos los campos del formulario.")

elif pagina == "Análisis e Historial":
    st.header("📊 Historial de Consultas")
    st.write("Registro local de todas las publicaciones generadas.")
    
    historial = obtener_historial()
    if historial:
        # Uso de st.dataframe para maquetar tablas de datos
        df = pd.DataFrame(historial)
        df_resumen = df.drop(columns=["resultado", "imagen_ia"], errors="ignore")
        st.dataframe(df_resumen, use_container_width=True)
        
        st.markdown("### 📝 Detalles de la Consulta")
        
        for i, registro in reversed(list(enumerate(historial))): # mostramos de la más reciente a la más antigua
            titulo_expander = f"📅 {registro.get('fecha', 'Sin fecha')} | 🧶 {registro.get('prenda', 'Sin prenda')} ➔ 🌍 {registro.get('mercado', 'Sin mercado')}"
            
            with st.expander(titulo_expander):
                st.write(f"**Material:** {registro.get('material', 'No especificado')}")
                st.write(f"**Color:** {registro.get('color', 'No especificado')}")
                st.write(f"**Talle (AR):** {registro.get('talle', 'No especificado')}")
                st.write(f"**Mercado:** {registro.get('mercado', 'No especificado')}")
                st.write(f"**Estado:** {registro['estado']}")
                
                st.write("**Resultado IA (Markdown):**")
                st.markdown(registro.get("resultado", "No hay resultado generado para esta consulta."))
                st.markdown("---")
                
                if st.button("🗑️ Borrar este registro", key=f"borrar_{i}"):
                    eliminar_consulta(i)
                    st.success("Registro borrado con éxito.")
                    st.rerun()
    else:
        st.info("Aún no hay consultas registradas.")