import os
import pandas as pd
from bertopic import BERTopic
from umap import UMAP
import pickle
import nltk
from nltk.corpus import stopwords
import re
import utils

# Descargar stopwords de NLTK
nltk.download("stopwords")
stop_words = set(stopwords.words("spanish"))

# Configuración
folder_path = "../linkedin_profiles"
output_path = "../bertopic_results.pkl"


# Función para eliminar stopwords y casos con `variable=valor`
def preprocess_text(text):
    text = re.sub(r'\b\w+=\S*\b', '', text)  # Elimina `variable=valor`
    tokens = text.split()
    cleaned_tokens = [word for word in tokens if word.lower() not in stop_words]
    return " ".join(cleaned_tokens)


# Cargar datos
linkedin_df = utils.load_data(folder_path)

# Preprocesar textos eliminando conectores y casos con `variable=valor`
linkedin_df["Processed_Text"] = (linkedin_df["Description"] + " " + linkedin_df["Aptitudes"]).dropna()
linkedin_df["Processed_Text"] = linkedin_df["Processed_Text"].apply(preprocess_text)
texts = linkedin_df["Processed_Text"].tolist()

# Verificar que los textos no estén vacíos
if len(texts) == 0:
    raise ValueError("No hay textos válidos después del preprocesamiento. Revisa los datos de entrada.")

# Configurar y entrenar BERTopic
umap_model = UMAP(n_neighbors=15, min_dist=0.1, n_components=2, metric="cosine", random_state=42)
topic_model = BERTopic(language="multilingual", umap_model=umap_model)
topics, probs = topic_model.fit_transform(texts)

# Excluir tópicos vacíos
topic_info = topic_model.get_topic_info()
topic_info = topic_info[topic_info["Count"] > 0]
print("Información general de los topics:")
print(topic_info)

# Imprimir palabras clave para los 5 primeros topics
print("\nTópicos principales y sus palabras clave:")
for topic_number in topic_info['Topic'][:5]:
    if topic_number != -1:
        print(f"Topic {topic_number}:")
        print(topic_model.get_topic(topic_number))

# Visualización de gráficos
try:
    print("\nMostrando distribución de tópicos...")
    topic_model.visualize_barchart(top_n_topics=10).show()

    print("Mostrando interrelaciones entre tópicos...")
    topic_model.visualize_topics().show()

    print("Mostrando representación de documentos y tópicos...")
    topic_model.visualize_documents(texts).show()
except Exception as e:
    print(f"Error al generar gráficos: {e}")

# Guardar resultados
with open(output_path, "wb") as f:
    pickle.dump({
        "model": topic_model,
        "texts": texts,
        "topics": topics,
        "probs": probs
    }, f)

print(f"Resultados de BERTopic guardados en: {output_path}")
