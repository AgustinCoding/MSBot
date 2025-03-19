from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import time
import pickle
from webdriver_manager.chrome import ChromeDriverManager


class Whatsapp:
    def _setupDriver(self):
        print("Configurando el driver de Chrome...")
        # Configurar ChromeDriver
        if not os.path.exists("browser_data"):
            print("Creando directorio 'browser_data'...")
            os.makedirs("browser_data")
        
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        
        if self.headless:
            print("Modo headless activado")
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
        
        user_data_dir = os.path.join(os.getcwd(), "browser_data", "chrome_profile")
        chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
        
        print("Instalando ChromeDriver...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("Driver configurado correctamente")
        
        return driver

    def __init__(self, headless=False, timeout=30):
        print("Inicializando la clase Whatsapp...")
        # Inicializar
        self.headless = headless
        self.timeout = timeout
        self.driver = self._setupDriver()
        self.is_logged_in = False
        self.cookie_file = os.path.join("browser_data", "whatsapp_cookies.pkl")
        print("Clase Whatsapp inicializada correctamente")
        
    def login(self, force_scan=False):
        print("Iniciando proceso de login...")
        # Iniciar sesion en WhatsApp Web
        self.driver.get("https://web.whatsapp.com/")
        print("Página de WhatsApp Web cargada")
        
        if os.path.exists(self.cookie_file) and not force_scan:
            try:
                print("Cargando cookies...")
                cookies = pickle.load(open(self.cookie_file, "rb"))
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
                self.driver.refresh()
                print("Cookies cargadas, refrescando la página...")
                
                logcheck_selector = "//h1[text()='Chats']"
                try:
                    print("Verificando si el login fue exitoso con cookies...")
                    WebDriverWait(self.driver, self.timeout).until(
                        EC.presence_of_element_located((By.XPATH, logcheck_selector))
                    )
                    self.is_logged_in = True
                    print("Sesion iniciada con cookies")
                    return True
                except TimeoutException:
                    print("No se pudo iniciar sesion con cookies")
            except Exception as e:
                print(f"Error al cargar cookies: {e}")
        
        print("Escanea el codigo QR en el navegador...")
        
        logcheck_selector = "//h1[text()='Chats']"
        try:
            print("Esperando a que el usuario escanee el código QR...")
            WebDriverWait(self.driver, 120).until(
                EC.presence_of_element_located((By.XPATH, logcheck_selector))
            )
            self.is_logged_in = True
            print("Sesion iniciada correctamente")
            
            cookies = self.driver.get_cookies()
            pickle.dump(cookies, open(self.cookie_file, "wb"))
            print("Cookies guardadas")
            
            return True
        except TimeoutException:
            print("No se pudo iniciar sesion")
            return False
        

    def openGroup(self, group_name):
        if not self.is_logged_in:
            print("No has iniciado sesion")
            return False
        try:
            filter_group_button = "group-filter"
            print("Encontrando grupo..")
            print("Buscando el botón de filtro de grupos...")
            button = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.ID, filter_group_button))
            )
            print("Botón de filtro de grupos encontrado")
            button.click()
            time.sleep(1)
            group_selector = f'//span[@title="{group_name}"]'
            print(f"Buscando el grupo: {group_name}")
            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.XPATH, group_selector))
            )
            print(f"Grupo {group_name} encontrado")
            
            group = self.driver.find_element(By.XPATH, group_selector)
            group.click()
            print(f"Grupo {group_name} seleccionado")
            time.sleep(2)
        except Exception:
            print("Error al abrir grupo")
            return False
            


    
    def send_message(self, message):

        try:
            message_box_selector = '//div[@aria-label="Escribe un mensaje"]//p'
            print("Buscando la caja de texto para enviar mensajes...")
            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.XPATH, message_box_selector))
            )
            print("Caja de texto encontrada")
            
            message_box = self.driver.find_element(By.XPATH, message_box_selector)
            message_box.clear()
            message_box.send_keys(message)
            print("Mensaje escrito en la caja de texto", '\n')

            print("Enviando..")
            time.sleep(0.5)
            message_box.send_keys(Keys.ENTER)
            print(f"Mensaje enviado al grupo.")
            return True
        
        except Exception as e:
            print(f"Error al enviar mensaje: {e}")
            return False

    def close(self):
        print("Cerrando sesión...")
        # Cerrar sesion
        if self.driver:
            self.driver.quit()
            print("Sesion cerrada")