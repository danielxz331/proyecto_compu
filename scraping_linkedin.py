from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from linkedin_scraper import Person
from googlesearch import search
import pickle
import os
import time

# Ruta para guardar perfiles y cookies
output_folder = "linkedin_profiles"
os.makedirs(output_folder, exist_ok=True)
cookies_file = "linkedin_cookies.pkl"

# Función para configurar y abrir el navegador
def open_browser():
    options = Options()
    options.add_argument("--start-maximized")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Función para guardar cookies
def save_cookies(driver):
    print("Guardando cookies...")
    with open(cookies_file, "wb") as file:
        pickle.dump(driver.get_cookies(), file)
    print("Cookies guardadas.")

# Función para cargar cookies
def load_cookies(driver):
    if os.path.exists(cookies_file):
        print("Cargando cookies...")
        driver.get("https://www.linkedin.com")
        with open(cookies_file, "rb") as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
        driver.refresh()
    else:
        print("No se encontraron cookies. Inicia sesión manualmente para guardarlas.")
        driver.get("https://www.linkedin.com/login")
        input("Inicia sesión en LinkedIn y presiona Enter para guardar las cookies...")
        save_cookies(driver)

# Función para procesar un perfil
def process_profile(profile_url):
    try:
        # Abrir navegador
        driver = open_browser()
        print(f"Abriendo navegador para: {profile_url}")

        # Cargar cookies para mantener la sesión
        load_cookies(driver)

        # Procesar el perfil
        person = Person(profile_url, driver=driver)
        person.scrape(close_on_complete=False)

        # Crear contenido para guardar
        user_data = (
            f"Nombre: {person.name}\n"
            f"Experiencia: {person.experiences}\n"
            f"Educación: {person.educations}\n"
            f"URL: {profile_url}\n"
            "-" * 40
        )

        # Guardar en archivo
        file_name = f"{output_folder}/{person.name.replace(' ', '_')}.txt"
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(user_data)

        print(f"Información guardada en: {file_name}")

        # Cerrar navegador
        driver.quit()
        return True
    except Exception as e:
        print(f"Error al procesar {profile_url}: {e}")
        if 'driver' in locals():
            driver.quit()
        return False


# Consulta en Google Search
query = 'site:linkedin.com "Ingeniería de Sistemas" OR "Ingeniería Electrónica" "Universidad de los Llanos"'
all_results = list(search(query, num_results=300))  # Recupera más resultados
profile_urls = [url for idx, url in enumerate(all_results) if idx >= 95 and 'linkedin.com/in/' in url]

# Archivo de registro para perfiles procesados
processed_file = "processed_profiles.txt"


# Cargar perfiles procesados desde el archivo
def load_processed_profiles():
    if os.path.exists(processed_file):
        with open(processed_file, "r", encoding="utf-8") as file:
            return set(file.read().splitlines())
    return set()


# Guardar perfiles procesados en el archivo
def save_processed_profile(profile_url):
    with open(processed_file, "a", encoding="utf-8") as file:
        file.write(profile_url + "\n")


# Procesar perfiles con verificación
processed_profiles = load_processed_profiles()

for index, profile_url in enumerate(profile_urls):
    if profile_url in processed_profiles:
        print(f"Perfil ya procesado, saltando: {profile_url}")
        continue
    
    print(f"Procesando perfil {index + 1}/{len(profile_urls)}: {profile_url}")
    success = process_profile(profile_url)
    
    if success:
        save_processed_profile(profile_url)
    else:
        print(f"No se pudo procesar el perfil: {profile_url}")
    
    time.sleep(5)  # Pausa para evitar bloqueos

