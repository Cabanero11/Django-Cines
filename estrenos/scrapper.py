import json
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configurar el logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_cine_ABC_ELX():
    edge_options = Options()
    edge_options.add_argument("--start-maximized")
    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=edge_options)

    try:
        driver.get('https://www.cinesabc.com/')
        
        logging.info("Página principal de Cines ABC cargada")

        # Aceptar cookies, sino no se puede interactuar con la pagina
        try:
            accept_cookies_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "avisoCookies__aceptar"))
            )
            accept_cookies_button.click()
            logging.info("Cookies aceptadas")
        except Exception as e:
            logging.info("No se encontró el botón de aceptar cookies o ya fue aceptado")

        # Esperar y buscar las carátulas de las películas
        caratulas = WebDriverWait(driver, 8).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'caratula'))
        )

        movies = {}

        for caratula in caratulas:
            try:
                image_element = caratula.find_element(By.CLASS_NAME, 'caratula__imagen')
                image_url = image_element.get_attribute('src')

                # Hacer clic en la carátula para ver los horarios
                image_element.click()

                # Esperar que la página de horarios se cargue
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID, 'trailer__titulo'))
                )

                # Obtener el título desde la ficha.php
                title_element_ficha = driver.find_element(By.ID, 'trailer__titulo')
                title = title_element_ficha.text.strip()

                # Buscar si "ABC ELX" está en la lista de cines
                cinema_elements = driver.find_elements(By.CLASS_NAME, 'cines__nombres')
                abc_elx_element = None

                for cinema_element in cinema_elements:
                    if "ABC ELX" in cinema_element.text:
                        abc_elx_element = cinema_element
                        break

                if abc_elx_element:
                    # Obtener el contenedor que tiene los horarios para "ABC ELX"
                    cinema_container = abc_elx_element.find_element(By.XPATH, './following-sibling::div[@class="cines__horas"]')
                    times_elements = cinema_container.find_elements(By.CLASS_NAME, 'boton_hora')

                    times = [{'time': time_element.text, 'ticket_url': time_element.get_attribute('data-link')} for time_element in times_elements]
                    
                    # Guardar la información en el diccionario de películas
                    movies[title] = {
                        'image_url': image_url,
                        'cinemas': [
                            {
                                'cinema_name': 'Cine ABC Elx',
                                'times': times
                            }
                        ]
                    }

                # Regresar a la página principal
                driver.back()

                # Esperar que las carátulas se carguen nuevamente
                WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, 'caratula'))
                )

            except Exception as e:
                logging.warning(f"Error al procesar la carátula: {e}")

        # Guardar los resultados en un archivo JSON
        with open('movies.json', 'w', encoding='utf-8') as f:
            json.dump(movies, f, ensure_ascii=False, indent=4)

        logging.info(f"Datos guardados en 'movies.json'")

    finally:
        driver.quit()
        logging.info("Scraper terminado y navegador cerrado")

if __name__ == "__main__":
    scrape_cine_ABC_ELX()
    logging.info('Scraping terminado !!!!')