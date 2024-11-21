import os
import pandas as pd
import re
from collections import Counter


TECH_NORMALIZATION = {
    "Python": "Python", "python": "Python",
    "JavaScript": "JavaScript", "javascript": "JavaScript", "js": "JavaScript",
    "TypeScript": "TypeScript", "typescript": "TypeScript", "ts": "TypeScript",
    "NodeJS": "Node.js", "node.js": "Node.js", "nodejs": "Node.js",
    "ReactJS": "React.js", "reactjs": "React.js", "react.js": "React.js",
    "AngularJS": "Angular", "angularjs": "Angular", "angular": "Angular",
    "VueJS": "Vue.js", "vue.js": "Vue.js", "vuejs": "Vue.js",
    "Django": "Django", "django": "Django",
    "Flask": "Flask", "flask": "Flask",
    "Spring Boot": "Spring Boot", "springboot": "Spring Boot", "spring boot": "Spring Boot",
    "Ruby on Rails": "Ruby on Rails", "rails": "Ruby on Rails", "ror": "Ruby on Rails",
    "Laravel": "Laravel", "laravel": "Laravel",
    "ASP.NET": "ASP.NET", "asp.net": "ASP.NET",
    "Postgres": "PostgreSQL", "PostgresQL": "PostgreSQL", "postgresql": "PostgreSQL",
    "MySQL": "MySQL", "mysql": "MySQL",
    "MongoDB": "MongoDB", "mongodb": "MongoDB",
    "Redis": "Redis", "redis": "Redis",
    "Sequelize.js": "Sequelize", "sequelize": "Sequelize",
    "TailwindCSS": "Tailwind CSS", "tailwind": "Tailwind CSS", "tailwindcss": "Tailwind CSS",
    "Bootstrap": "Bootstrap", "bootstrap": "Bootstrap",
    "TensorFlow": "TensorFlow", "tensorflow": "TensorFlow",
    "PyTorch": "PyTorch", "pytorch": "PyTorch",
    "Kubernetes": "Kubernetes", "k8s": "Kubernetes", "kubernetes": "Kubernetes",
    "Docker": "Docker", "docker": "Docker",
    "Jenkins": "Jenkins", "jenkins": "Jenkins",
    "Git": "Git", "git": "Git",
    "GitHub": "GitHub", "github": "GitHub",
    "GitLab": "GitLab", "gitlab": "GitLab",
    "Bitbucket": "Bitbucket", "bitbucket": "Bitbucket",
    "Vite": "Vite", "vite": "Vite",
    "Webpack": "Webpack", "webpack": "Webpack",
    "Raspberry": "Raspberry Pi", "RaspberryPi": "Raspberry Pi", "raspberry pi": "Raspberry Pi",
    "Arduino": "Arduino", "arduino": "Arduino",
    "Express": "Express.js", "expressjs": "Express.js", "express.js": "Express.js",
    "FastAPI": "FastAPI", "fastapi": "FastAPI",
    "NextJS": "Next.js", "nextjs": "Next.js", "next.js": "Next.js",
    "NuxtJS": "Nuxt.js", "nuxtjs": "Nuxt.js", "nuxt.js": "Nuxt.js",
    "Svelte": "Svelte", "svelte": "Svelte",
    "Flutter": "Flutter", "flutter": "Flutter",
    "React Native": "React Native", "reactnative": "React Native", "react native": "React Native"
}

CARGOS_NORMALIZATION = {
    "Administradora de bases de datos": "Administradora de bases de datos",
    "Analista Seguridad": "Analista Seguridad",
    "Analista de Información": "Analista de Información",
    "Analista de desarrollo TI": "Analista de desarrollo TI",
    "Analista de soporte TI": "Analista de soporte TI",
    "Aprendiz": "Aprendiz",
    "Arquitecto Empresarial": "Arquitecto Empresarial",
    "Arquitecto de Negocio Positiva Compañia de seguros": "Arquitecto de Negocio Positiva Compañia de seguros",
    "Asistente AWS": "Asistente AWS",
    "Auxiliar administrativo": "Auxiliar administrativo",
    "Auxiliar de sistemas": "Auxiliar de sistemas",
    "Auxiliar docente": "Auxiliar docente",
    "Auxiliar docente y Monitor": "Auxiliar docente y Monitor",
    "Backend Developer": "Backend Developer",
    "Becario": "Becario",
    "Bilingual Customer Service Representative": "Bilingual Customer Service Representative",
    "Catedrático": "Catedrático",
    "Chief Executive Officer": "Chief Executive Officer",
    "Computer Programmer": "Computer Programmer",
    "Consultor": "Consultor",
    "Consultor Seguridad de la Información": "Consultor Seguridad de la Información",
    "Consultor TI": "Consultor TI",
    "Consultor de gestión empresarial": "Consultor de gestión empresarial",
    "Consultor de programación": "Consultor de programación",
    "Consultor en productividad de Sw": "Consultor en productividad de Sw",
    "Coordinador Mesa de Ayuda - Help Desk": "Coordinador Mesa de Ayuda - Help Desk",
    "Coordinador Proyecto Formación TIC": "Coordinador Proyecto Formación TIC",
    "Coordinador académico - medio tiempo": "Coordinador académico - medio tiempo",
    "Coordinador de Programa - Unidad de Ingeniería y Ciencias Básicas": "Coordinador de Programa - Unidad de Ingeniería y Ciencias Básicas",
    "Coordinador de conectividad": "Coordinador de conectividad",
    "Coordinador de formación areas tecnicas": "Coordinador de formación areas tecnicas",
    "Coordinador del programa de Ingeniería de Sistemas": "Coordinador del programa de Ingeniería de Sistemas",
    "Coordinadora académica": "Coordinadora académica",
    "Data Analyst": "Data Analyst",
    "Data Scientist": "Data Scientist",
    "Desarrollador": "Desarrollador",
    "Desarrollador Frontend": "Desarrollador Frontend",
    "Desarrollador Full Stack Django": "Desarrollador Full Stack Django",
    "Desarrollador Fullstack": "Desarrollador Fullstack",
    "Desarrollador de aplicaciones para móviles": "Desarrollador de aplicaciones para móviles",
    "Desarrollador de back-end": "Desarrollador de back-end",
    "Desarrollador de hardware": "Desarrollador de hardware",
    "Desarrollador de software": "Desarrollador de software",
    "Desarrollador web": "Desarrollador web",
    "Desarrolladora • Contratista": "Desarrolladora • Contratista",
    "Developer Back-End (php)": "Developer Back-End (php)",
    "Director de Programa Ingeniería de Sistemas": "Director de Programa Ingeniería de Sistemas",
    "Director de software": "Director de software",
    "Directora Académica": "Directora Académica",
    "Directora del Departamento de Extensión": "Directora del Departamento de Extensión",
    "Docente": "Docente",
    "Docente Catedrático": "Docente Catedrático",
    "Docente Ingenieria Electronica": "Docente Ingenieria Electronica",
    "Docente catedrático": "Docente catedrático",
    "Docente de la Especialización en Ingeniería de Software": "Docente de la Especialización en Ingeniería de Software",
    "Docente de la Maestría en Gestión y Desarrollo de Proyectos de Software": "Docente de la Maestría en Gestión y Desarrollo de Proyectos de Software",
    "Docente medio tiempo": "Docente medio tiempo",
    "Docente ocacional tc": "Docente ocacional tc",
    "Docente tiempo completo": "Docente tiempo completo",
    "EPM Consultant": "EPM Consultant",
    "Electronic Technician I": "Electronic Technician I",
    "Estudiante": "Estudiante",
    "Estudiante de Ingeniería": "Estudiante de Ingeniería",
    "Estudiante de doctorado": "Estudiante de doctorado",
    "Experto SIG": "Experto SIG",
    "Freelance Programmer": "Freelance Programmer",
    "Full Stack Developer": "Full Stack Developer",
    "Full-stack Developer": "Full-stack Developer",
    "Gerente": "Gerente",
    "Gerente General": "Gerente General",
    "Gerente de Proyecto": "Gerente de Proyecto",
    "Gestor": "Gestor",
    "Gestor Técnico": "Gestor Técnico",
    "Gestor de TI": "Gestor de TI",
    "INGENIERO ELECTRONICO": "INGENIERO ELECTRONICO",
    "INGENIERO ELECTRÓNICO EN CARACTERIZACION": "INGENIERO ELECTRÓNICO EN CARACTERIZACION",
    "Information Technology Consultant": "Information Technology Consultant",
    "Ingeniera de soporte y desarrollo": "Ingeniera de soporte y desarrollo",
    "Ingeniera electrónica": "Ingeniera electrónica",
    "Ingeniero Electronico Desarrollador": "Ingeniero Electronico Desarrollador",
    "Ingeniero Supervisor": "Ingeniero Supervisor",
    "Ingeniero de Comunicaciones y Seguridad Informática": "Ingeniero de Comunicaciones y Seguridad Informática",
    "Ingeniero de Instrumentación y Control": "Ingeniero de Instrumentación y Control",
    "Ingeniero de Precomisionamiento Instrumentación y Control": "Ingeniero de Precomisionamiento Instrumentación y Control",
    "Ingeniero de Sistemas": "Ingeniero de Sistemas",
    "Ingeniero de campo": "Ingeniero de campo",
    "Ingeniero de desarrollo de software": "Ingeniero de desarrollo de software",
    "Ingeniero de proyecto": "Ingeniero de proyecto",
    "Ingeniero de proyectos": "Ingeniero de proyectos",
    "Ingeniero de software": "Ingeniero de software",
    "Ingeniero electrónico": "Ingeniero electrónico",
    "Java Software Developer": "Java Software Developer",
    "Jefe comercial": "Jefe comercial",
    "Jefe de Universidad Corporativa": "Jefe de Universidad Corporativa",
    "Lider Regional": "Lider Regional",
    "Negocios internacionales": "Negocios internacionales",
    "Oficial de Seguridad de la Información": "Oficial de Seguridad de la Información",
    "Pasante en Ingeniería Electrónica": "Pasante en Ingeniería Electrónica",
    "Practicante en Ingeniería de Sistemas": "Practicante en Ingeniería de Sistemas",
    "Profesor Ocasional": "Profesor Ocasional",
    "profesora universitaria": "profesora universitaria"
}


def load_data(folder_path):
    files = os.listdir(folder_path)
    data = []
    for file in files:
        file_path = os.path.join(folder_path, file)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            description = re.search(r"description:(.*?)(\n|$)", content, re.IGNORECASE)
            aptitudes = re.search(r"aptitudes:(.*?)(\n|$)", content, re.IGNORECASE)
            duration = re.search(r"duration='(.*?)'", content, re.IGNORECASE)
            position_title = re.search(r"position_title='(.*?)'", content, re.IGNORECASE)
            data.append({
                "Description": description.group(1).strip() if description else "",
                "Aptitudes": aptitudes.group(1).strip() if aptitudes else "",
                "Duration": duration.group(1).strip() if duration else "",
                "Position_Title": position_title.group(1).strip() if position_title else ""
            })
    return pd.DataFrame(data)


def normalize_technologies(tech_list, normalization_dict):
    normalized = []
    for tech in tech_list:
        for key, value in normalization_dict.items():
            if re.search(rf"\b{re.escape(key)}\b", tech, re.IGNORECASE):
                normalized.append(value)
                break
    return list(set(normalized))


def extract_positions(df, column_name, normalization_dict):
    def normalize_position(position):
        if not isinstance(position, str):
            return None
        for key, value in normalization_dict.items():
            if key.lower() in position.lower():
                return value
        return "Otro"

    df["Extracted_Positions"] = df[column_name].apply(normalize_position)
    return df


def generate_position_statistics(df, column_name):
    stats = df[column_name].value_counts().reset_index()
    stats.columns = ["Position", "Count"]
    return stats


def extract_technologies(df, description_col, aptitudes_col, normalization_dict):
    df["Extracted_Tech"] = df.apply(
        lambda row: normalize_technologies(row[description_col].split() + row[aptitudes_col].split(), normalization_dict),
        axis=1
    )
    return df


def parse_duration(duration_text):
    match = re.search(r"(\d+)\s*año[s]?\s*(\d+)?\s*mes[es]?", duration_text, re.IGNORECASE)
    if match:
        years = int(match.group(1))
        months = int(match.group(2)) if match.group(2) else 0
        return years + (months / 12)
    return 0


def generate_statistics(df, tech_col):
    all_techs = [tech for tech_list in df[tech_col] for tech in tech_list]
    tech_counts = Counter(all_techs)
    stats_df = pd.DataFrame.from_dict(tech_counts, orient="index", columns=["Frequency"]).reset_index()
    stats_df.rename(columns={"index": "Technology"}, inplace=True)
    return stats_df