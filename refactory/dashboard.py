import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud
import pickle
import utils


folder_path = "../linkedin_profiles"
bertopic_path = "../bertopic_results.pkl"


linkedin_df = utils.load_data(folder_path)
linkedin_df = utils.extract_technologies(linkedin_df, "Description", "Aptitudes", utils.TECH_NORMALIZATION)
linkedin_df["Years_Experience"] = linkedin_df["Duration"].apply(utils.parse_duration)
linkedin_df = utils.extract_positions(linkedin_df, "Position_Title", utils.CARGOS_NORMALIZATION)


tech_stats = utils.generate_statistics(linkedin_df, "Extracted_Tech")
position_stats = utils.generate_position_statistics(linkedin_df, "Extracted_Positions")
average_experience = linkedin_df["Years_Experience"].mean()
years_experience = linkedin_df["Years_Experience"].dropna().tolist()


with open(bertopic_path, "rb") as f:
    bertopic_data = pickle.load(f)

topic_model = bertopic_data["model"]

st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://www.asosupro.gov.co/admin/uploads/blog/lg-26-logo-unillanos.png" alt="Logo" style="width: 150px; margin-bottom: 20px;">
    </div>
    """,
    unsafe_allow_html=True
)

st.title("Explorando el Talento Tecnológico: Análisis de Perfiles de Linkedin de la Universidad de los llanos 📊")


st.markdown("""
### Introducción
Este dashboard nos lleva a través de un recorrido fascinante sobre el panorama de habilidades tecnológicas, cargos ocupados y experiencia profesional identificados en perfiles de LinkedIn. ¿Qué tecnologías dominan? ¿Qué posiciones son más comunes? ¿Cómo se distribuye la experiencia en la industria? Acompáñanos mientras desentrañamos estas historias.
""")


st.subheader("Estadísticas de Tecnologías")
st.markdown("""
*Dominio del ecosistema digital*
La tabla a continuación muestra el ranking de tecnologías más destacadas en los perfiles analizados. JavaScript lidera con una frecuencia de 7, seguido de Python y bases de datos como PostgreSQL y MySQL, con 6 menciones cada uno. 
Estas tecnologías son esenciales en el desarrollo web y backend. Si buscas destacar en el mercado laboral, dominarlas puede ser un excelente punto de partida.
""")


def highlight_top_technologies(row):
    if row["Frequency"] >= tech_stats["Frequency"].max():
        return ['background-color: #ffdd57'] * len(row)  
    elif row["Frequency"] >= tech_stats["Frequency"].mean():
        return ['background-color: #c3e6cb'] * len(row) 
    else:
        return [''] * len(row)  #


st.subheader("Tecnologías Más Usadas (Resaltadas por Frecuencia)")
styled_df = tech_stats.style.apply(highlight_top_technologies, axis=1)
st.write(styled_df.to_html(), unsafe_allow_html=True)


st.subheader("Gráfico de Tecnologías Más Usadas")
st.markdown("""
El siguiente gráfico refuerza la importancia de estas tecnologías en el ecosistema actual. Además, herramientas como Tailwind CSS y GitHub aparecen como imprescindibles en diseño y colaboración.
""")
fig_tech = px.bar(
    tech_stats,
    x="Technology",
    y="Frequency",
    title="Tecnologías Más Usadas",
    labels={"Technology": "Tecnología", "Frequency": "Frecuencia"}
)
fig_tech.update_layout(template="plotly_white", title_x=0.5)
st.plotly_chart(fig_tech)


st.subheader("Nube de Palabras de Tecnologías")
st.markdown("""
La nube de palabras nos permite visualizar el protagonismo de las tecnologías mencionadas. Observamos que JavaScript, PostgreSQL y Python dominan, pero también hay diversidad con herramientas como Docker y Vue.js, destacando la amplitud del ecosistema.
""")
if not tech_stats.empty:
    wordcloud = WordCloud(width=800, height=400).generate(" ".join(tech_stats["Technology"]))
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    st.pyplot(plt)
else:
    st.write("No hay datos suficientes para generar la nube de palabras.")


st.subheader("Cargos Ocupados")
st.markdown("""
*Diversidad profesional*
Al analizar los cargos ocupados, vemos que "Estudiante" lidera, reflejando una gran cantidad de talento emergente. Sin embargo, roles como "Desarrollador" e "Ingeniero de software" también destacan, mostrando una alta demanda en estas áreas.
""")
fig_positions = px.bar(
    position_stats,
    x="Position",
    y="Count",
    title="Frecuencia de Cargos Ocupados",
    labels={"Position": "Cargo", "Count": "Frecuencia"}
)
fig_positions.update_layout(template="plotly_white", title_x=0.5)
st.plotly_chart(fig_positions)


st.subheader("Años de Experiencia")
st.markdown(f"""
*Un promedio prometedor*
El promedio de experiencia identificado es de {average_experience:.2f} años. Esto indica una mezcla de talento joven con profesionales en ascenso. La mayoría de los perfiles se concentran entre 0 y 2 años, destacando el continuo ingreso de nuevos talentos al mercado.
""")
st.metric("Promedio de Años de Experiencia", f"{average_experience:.2f} años")

fig_exp = px.histogram(
    linkedin_df,
    x="Years_Experience",
    nbins=10,
    title="Distribución de Años de Experiencia",
    labels={"Years_Experience": "Años de Experiencia"}
)
fig_exp.update_layout(template="plotly_white", title_x=0.5)
st.plotly_chart(fig_exp)


st.subheader("Tópicos Identificados por BERTopic")
st.markdown("""
*Análisis profundo del contenido*
Gracias a BERTopic, identificamos patrones en los textos analizados. Estos resultados ayudan a explorar cómo estructurar mejor las descripciones y destacar habilidades únicas.
""")
fig1 = topic_model.visualize_barchart(top_n_topics = 1, n_words = 15)
st.plotly_chart(fig1)


st.markdown("""
### Conclusión: Un panorama lleno de oportunidades
Este análisis no solo nos ofrece estadísticas y gráficos, sino también historias sobre las tecnologías que moldean el presente, los roles más demandados y el prometedor talento emergente. Si eres un profesional buscando crecer o una empresa buscando contratar, este dashboard es un mapa invaluable del ecosistema tecnológico actual.
""")