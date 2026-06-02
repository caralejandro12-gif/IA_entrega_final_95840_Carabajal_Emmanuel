# Documentación: Artelanitas Global E-commerce AI 🧶

Este documento centraliza los prompts, la arquitectura y los conceptos técnicos más importantes aplicados en el desarrollo del Producto Mínimo Viable (MVP) para la internacionalización del catálogo de Artelanitas.

---

## 1. El Prompt Principal (Ingeniería de Prompts Avanzada)

El corazón de la aplicación es un prompt parametrizado que utiliza técnicas de delimitación de roles, restricciones estrictas y formateo de salida (Markdown). Además, está diseñado para ser **multimodal** (procesa texto e imágenes simultáneamente).

**Texto del Prompt Base:**
> Actúa como un equipo experto: Especialista en E-commerce, Copywriter y Analista SEO.
> Crea una publicación de venta de alto impacto para la tienda de tejidos 'Artelanitas'.
> 
> Contexto: Productos tejidos a mano, premium. 
> REGLA ESTRICTA: La línea de productos es de uso exclusivo para personas. Bajo ninguna circunstancia incluyas conceptos, palabras clave o sugerencias de que los productos son 'pet-friendly'.
> 
> Entrada:
> - Prenda: {prenda}
> - Material: {material}
> - Color: {color}
> - Talle origen (Argentina): {talle}
> - País de destino: {pais}
> 
> *(Si el usuario adjunta una foto, se inyecta dinámicamente esta instrucción)*:
> Analiza minuciosamente la imagen adjunta para describir la textura, el grosor, el patrón del punto de tejido y el acabado visual real de la prenda. Incluye estos detalles visuales en la Descripción Persuasiva y en las Características Técnicas.
> 
> Salida en Markdown en el idioma de {pais}:
> 1. Título SEO (máx 60 caracteres).
> 2. Descripción Persuasiva (Storytelling).
> 3. Características Técnicas (Bullet points).
> 4. Guía de Talles (Equivalencia de {talle} al estándar de {pais}).
> 5. Etiquetas SEO (10 tags separados por comas).

---

## 2. Arquitectura del Proyecto

El proyecto sigue el principio de **Clean Code** (Código Limpio) separando las responsabilidades en módulos lógicos:

* **`app.py` (Frontend):** Interfaz gráfica desarrollada con `streamlit`. Maneja el enrutamiento (menú lateral), los formularios de entrada de datos, la subida de imágenes y la visualización del historial.
* **`utils/api_handler.py` (Cerebro/API):** Encapsula toda la lógica de conexión con Google Gemini. Recibe los parámetros del frontend, ensambla el prompt y devuelve la respuesta generada.
* **`utils/storage.py` (Base de Datos):** Maneja la persistencia de datos local creando y gestionando un archivo `history.json`. Contiene las funciones del CRUD: `guardar_consulta()`, `obtener_historial()` y `eliminar_consulta()`.

---

## 3. Puntos Técnicos Clave (Buenas Prácticas Aplicadas)

### A. Uso del SDK Moderno de Google
Se abandonó la librería legacy en favor de la actual **`google-genai`**. Se utiliza el modelo **`gemini-2.5-flash`**, que destaca por su velocidad y su capacidad nativa para recibir listas combinadas de texto y objetos de imagen (`PIL.Image`).

### B. Persistencia de Datos y Manejo de Errores
Para evitar caídas de la aplicación (crashes), se implementaron las siguientes estrategias en la gestión del archivo JSON:
* **Gestión de archivos vacíos:** Uso de `try/except json.JSONDecodeError` para detectar si el archivo JSON está vacío o corrupto, inicializando una lista vacía `[]` automáticamente sin romper el flujo.
* **Acceso seguro a diccionarios:** Uso del método `.get('clave', 'valor_por_defecto')` en lugar de corchetes `['clave']` para renderizar el historial. Esto previene errores `KeyError` cuando se consultan registros antiguos que no poseían los nuevos campos agregados.

### C. Dinamismo en la Interfaz (Streamlit)
* Uso de `st.expander` para mantener una interfaz limpia al mostrar textos largos generados por la IA.
* Implementación de `st.rerun()` para actualizar instantáneamente la pantalla cuando el usuario elimina un registro de la base de datos, mejorando la experiencia de usuario (UX).

### D. Seguridad y Despliegue (Deploy)
* **Protección de Credenciales:** Uso exclusivo de variables de entorno mediante un archivo `.env` local y la librería `python-dotenv`.
* **Control de Versiones Seguro:** Inclusión de un archivo `.gitignore` para asegurar que el archivo `.env` nunca se suba al repositorio público de GitHub.
* **Cloud Deployment:** Configuración de la `GEMINI_API_KEY` directamente en los *Secrets* de Streamlit Community Cloud para habilitar el funcionamiento de la aplicación en producción.