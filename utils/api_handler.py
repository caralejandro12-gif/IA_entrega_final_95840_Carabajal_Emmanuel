import os
import google.genai as genai
from dotenv import load_dotenv

# Cargar variables de entorno de forma segura
load_dotenv()

# Configurar la API
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    client = genai.Client(api_key=api_key)
else:
    client = None
    print("Error: API Key no encontrada en el archivo .env")


def generar_catalogo_ia(prenda, material, color, talle, pais, imagen=None):
    """
    Se comunica con la API de Gemini para generar el copy del producto.
    Si recibe una imagen, la procesa de forma multimodal para enriquecer la descripción.
    """
    if not client:
        return "Error: API Key no configurada o no encontrada en el archivo .env."

    prompt = f"""
    Actúa como un equipo experto: Especialista en E-commerce, Copywriter y Analista SEO.
    Crea una publicación de venta de alto impacto para la tienda de tejidos 'Artelanitas', enfocada en el mercado de {pais}.
    Se eficaz, persuasivo y adapta el lenguaje al público objetivo de ese país.
    
    Contexto: Productos tejidos a mano, premium. 
    REGLA ESTRICTA: Productos de uso exclusivo para personas, no para animales ni objetos. No generar contenido para usos no humanos.
    
    Entrada:
    - Prenda: {prenda}
    - Material: {material}
    - Color: {color}
    - Talle origen (Argentina): {talle}
    - País de destino: {pais}
    """

    if imagen:
        prompt += "\nAnaliza minuciosamente la imagen adjunta para describir la textura, el grosor, el patrón del punto de tejido y el acabado visual real de la prenda. Incluye estos detalles visuales en la Descripción Persuasiva y en las Características Técnicas."

    prompt += f"""
    Salida en Markdown en el idioma de {pais}:
    1. Título SEO (máx 30 caracteres).
    2. Descripción Persuasiva (Storytelling).
    3. Características Técnicas (Bullet points).
    4. Guía de Talles (Equivalencia de {talle} al estándar de {pais}).
    5. Etiquetas SEO (10 tags separados por comas).
    """
    
    if imagen:
        contents = [prompt, imagen]
    else:
        contents = prompt
    try:
        respuesta = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=contents
        )
        return respuesta.text
    except Exception as e:
        return f"Error al conectar con la IA: {e}"