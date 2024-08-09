import json
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

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
        caratulas = WebDriverWait(driver, 14).until(
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


### 2º Funcion de scrap
def scrape_cine_imf_torrevieja():
    edge_options = Options()
    edge_options.add_argument("--start-maximized")
    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=edge_options)

    try:
        driver.get('https://cine.entradas.com/cine/torrevieja/imf-torrevieja/sesiones/')
        
        logging.info("Página de IMF Torrevieja cargada")

        # Aceptar cookies
        try:
            accept_cookies_button = WebDriverWait(driver, 12).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@title='Aceptar todo']"))
            )
            accept_cookies_button.click()
            logging.info("Cookies aceptadas")
        except Exception as e:
            logging.info("No se encontró el botón de aceptar cookies o ya fue aceptado")

        # Hacer scroll hasta la sección de horarios para cargar contenido
        logging.info("Comenzando a desplazar hasta la sección de horarios...")
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollBy(0, window.innerHeight);")  # Baja una pantalla completa
            time.sleep(2)  # Esperar a que se cargue más contenido
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                logging.info("Se ha alcanzado el final de la página.")
                break
            last_height = new_height
        
        # Volver al inicio de la página
        driver.execute_script("window.scrollTo(0, 0);")
        logging.info("Se ha vuelto al inicio de la página.")

        # Obtener el HTML de la página después de scroll
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        movies = {}

        # Buscar todas las películas
        movie_elements = soup.find_all('div', class_='text-dark dark:text-light space-x-2 text-xl font-medium leading-tight md:text-2xl')
        for movie_element in movie_elements:
            title = movie_element.get_text(strip=True)

            # Obtener la imagen de la película
            image_element = movie_element.find_previous('img')
            image_url = image_element['src'] if image_element else None

            # Asegurarse de que todos los botones "Mostrar más" sean presionados
            try:
                # Recolectar todos los botones "Mostrar más"
                mostrar_mas_buttons = driver.find_elements(By.XPATH, "//button[@title='Mostrar más']")
                for button in mostrar_mas_buttons:
                    # Usar WebDriverWait para asegurarse de que el botón esté visible y clicable
                    WebDriverWait(driver, 6).until(
                        EC.element_to_be_clickable(button)
                    )
                    driver.execute_script("arguments[0].scrollIntoView(true);", button)
                    button.click()
                    logging.info(f"Botón 'Mostrar más' para la película: {title} pulsado")
                    time.sleep(1)  # Dar tiempo para que cargue más contenido
            except Exception as e:
                logging.warning(f"No se pudo pulsar el botón 'Mostrar más' para la película: {title} - {e}")
            # Obtener el contenedor de horarios que tiene la columna "Hoy"
            schedules_container = movie_element.find_next('div', class_='space-y-2')

            if not schedules_container:
                logging.warning(f"No se encontró el contenedor de horarios para la película: {title}")
                continue

            # Limitar a los horarios del primer día
            all_times = []
            schedule_divs = schedules_container.find_all('div', class_='w-full items-center space-y-3 text-center')

            # Filtrar solo el primer grupo de horarios
            if schedule_divs:
                first_schedule_div = schedule_divs[0]
                time_elements = first_schedule_div.find_all('div', class_='text-on-neutral flex h-11 items-center justify-center')
                for time_element in time_elements:
                    time_text = time_element.get_text(strip=True)
                    ticket_url = 'https://cine.entradas.com' + time_element.find_previous('a')['href']
                    all_times.append({'time': time_text, 'ticket_url': ticket_url})

            # Guardar la información en el diccionario de películas
            movies[title] = {
                'image_url': image_url,
                'cinemas': [
                    {
                        'cinema_name': 'IMF Torrevieja',
                        'times': all_times  # Aquí se guardan solo los horarios del primer día
                    }
                ]
            }

        # Guardar los resultados en un archivo JSON
        with open('movies_imf_torrevieja.json', 'w', encoding='utf-8') as f:
            json.dump(movies, f, ensure_ascii=False, indent=4)

        logging.info(f"Datos guardados en 'movies_imf_torrevieja.json'")

    finally:
        driver.quit()
        logging.info("Scraper terminado y navegador cerrado")


if __name__ == "__main__":
    #scrape_cine_ABC_ELX()
    # Probamos 1 a uno a ver
    scrape_cine_imf_torrevieja()
    logging.info('Scraping terminado !!!!')