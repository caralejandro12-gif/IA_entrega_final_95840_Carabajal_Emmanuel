import json
import os

FILE_PATH = "data/history.json"

def asegurar_directorio():
    """Crea el directorio y el archivo si no existen."""
    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump([], f)

def guardar_consulta(datos_consulta):
    """Guarda un diccionario de datos en el archivo JSON."""
    asegurar_directorio()
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        historial = json.load(f)
        
    historial.append(datos_consulta)
    
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(historial, f, indent=4, ensure_ascii=False)

def obtener_historial():
    """Devuelve la lista de consultas guardadas."""
    asegurar_directorio()
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def eliminar_consulta(indice):
    """Elimina un registro específico del historial usando su índice y guarda los cambios."""
    historial = obtener_historial()
    
    # Verificamos que el índice sea válido
    if 0 <= indice < len(historial):
        historial.pop(indice) # Elimina el elemento de la lista
        
        # Guardamos la lista actualizada en el JSON
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(historial, f, indent=4, ensure_ascii=False)
        return True
    return False