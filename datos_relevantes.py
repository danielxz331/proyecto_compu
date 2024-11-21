import os
import pandas as pd
import re
from collections import Counter


# Función para extraer información clave
def extract_information(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # Separar por líneas y extraer secciones clave
        lines = content.split("\n")
        description = next((line.replace("description:", "").strip() for line in lines if "description:" in line.lower()), "")
        experience = next((line.replace("Experiencia:", "").strip() for line in lines if "Experiencia:" in line), "")
        education = next((line.replace("Educación:", "").strip() for line in lines if "Educación:" in line), "")
        return {"Description": description, "Experience": experience, "Education": education}
    except Exception as e:
        return {"Description": "", "Experience": "", "Education": "", "Error": str(e)}


# Función para limpiar texto y extraer palabras clave
def clean_and_extract_keywords(text):
    if not isinstance(text, str):
        return []
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)  # Eliminar caracteres especiales
    keywords = text.split()
    return keywords


# Cargar datos desde los archivos
def load_data(folder_path):
    files = os.listdir(folder_path)
    data = []
    for file in files:
        file_path = os.path.join(folder_path, file)
        info = extract_information(file_path)
        data.append(info)
    return pd.DataFrame(data)


# Ruta a la carpeta de datos
linkedin_profiles_folder = "linkedin_profiles"
linkedin_df = load_data(linkedin_profiles_folder)

# Procesar datos para estadísticas
linkedin_df["Keywords"] = linkedin_df["Description"].apply(clean_and_extract_keywords)

# Obtener estadísticas de palabras clave (e.g., lenguajes, herramientas)
all_keywords = [keyword for keywords in linkedin_df["Keywords"] for keyword in keywords]
keyword_counts = Counter(all_keywords)

# Calcular años de experiencia promedio (ejemplo simplificado)
linkedin_df["Years_Experience"] = linkedin_df["Experience"].apply(lambda x: re.findall(r"(\d+)\s+año", x.lower()))
linkedin_df["Years_Experience"] = linkedin_df["Years_Experience"].apply(lambda x: sum(map(int, x)) if x else 0)
average_experience = linkedin_df["Years_Experience"].mean()

# Mostrar estadísticas
print("Lenguajes y Tecnologías más comunes:")
print(keyword_counts.most_common(10))
print(f"Años de experiencia promedio: {average_experience:.2f}")
