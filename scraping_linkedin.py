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


output_folder = "linkedin_profiles"
os.makedirs(output_folder, exist_ok=True)
cookies_file = "linkedin_cookies.pkl"


def open_browser():
    options = Options()
    options.add_argument("--start-maximized")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def save_cookies(driver):
    print("Guardando cookies...")
    with open(cookies_file, "wb") as file:
        pickle.dump(driver.get_cookies(), file)
    print("Cookies guardadas.")


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


def process_profile(profile_url):
    try:
        driver = open_browser()
        print(f"Abriendo navegador para: {profile_url}")

        load_cookies(driver)

        person = Person(profile_url, driver=driver)
        person.scrape(close_on_complete=False)

        user_data = (
            f"Nombre: {person.name}\n"
            f"Experiencia: {person.experiences}\n"
            f"Educación: {person.educations}\n"
            f"URL: {profile_url}\n"
            "-" * 40
        )

        file_name = f"{output_folder}/{person.name.replace(' ', '_')}.txt"
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(user_data)

        print(f"Información guardada en: {file_name}")

        driver.quit()
        return True
    except Exception as e:
        print(f"Error al procesar {profile_url}: {e}")
        if 'driver' in locals():
            driver.quit()
        return False


query = 'site:linkedin.com "Ingeniería de Sistemas" OR "Ingeniería Electrónica" "Universidad de los Llanos"'
all_results = list(search(query, num_results=300))
profile_urls = [url for idx, url in enumerate(all_results) if idx >= 95 and 'linkedin.com/in/' in url]


processed_file = "processed_profiles.txt"


def load_processed_profiles():
    if os.path.exists(processed_file):
        with open(processed_file, "r", encoding="utf-8") as file:
            return set(file.read().splitlines())
    return set()


def save_processed_profile(profile_url):
    with open(processed_file, "a", encoding="utf-8") as file:
        file.write(profile_url + "\n")


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
    
    time.sleep(5)

