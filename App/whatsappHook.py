from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import time
import requests
import zipfile
import platform
import json
import pickle
from webdriver_manager.chrome import ChromeDriverManager


class Whatsapp:
    def _setupDriver(self):
        # Configurar ChromeDriver
        if not os.path.exists("browser_data"):
            os.makedirs("browser_data")
        
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        
        if self.headless:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
        
        user_data_dir = os.path.join(os.getcwd(), "browser_data", "chrome_profile")
        chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        return driver

    def __init__(self, headless=False, timeout=30):
        # Inicializar
        self.headless = headless
        self.timeout = timeout
        self.driver = self._setupDriver()
        self.is_logged_in = False
        self.cookie_file = os.path.join("browser_data", "whatsapp_cookies.pkl")
        
    def login(self, force_scan=False):
        # Iniciar sesion en WhatsApp Web
        self.driver.get("https://web.whatsapp.com/")
        
        if os.path.exists(self.cookie_file) and not force_scan:
            try:
                cookies = pickle.load(open(self.cookie_file, "rb"))
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
                self.driver.refresh()
                print("Intentando iniciar sesion con cookies...")
                
                chat_list_selector = '//div[@data-testid="chat-list"]'
                try:
                    WebDriverWait(self.driver, self.timeout).until(
                        EC.presence_of_element_located((By.XPATH, chat_list_selector))
                    )
                    self.is_logged_in = True
                    print("Sesion iniciada con cookies")
                    return True
                except TimeoutException:
                    print("No se pudo iniciar sesion con cookies")
            except Exception as e:
                print(f"Error al cargar cookies: {e}")
        
        print("Escanea el codigo QR en el navegador...")
        
        chat_list_selector = '//div[@data-testid="chat-list"]'
        try:
            WebDriverWait(self.driver, 120).until(
                EC.presence_of_element_located((By.XPATH, chat_list_selector))
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
    
    def send_group_message(self, group_name, message):
        # Enviar mensaje a un grupo
        if not self.is_logged_in:
            print("No has iniciado sesion")
            return False
        
        try:
            self.driver.get("https://web.whatsapp.com/")
            time.sleep(3)
            
            search_box_selector = '//div[@contenteditable="true"][@data-testid="chat-list-search"]'
            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.XPATH, search_box_selector))
            )
            
            search_box = self.driver.find_element(By.XPATH, search_box_selector)
            search_box.clear()
            search_box.send_keys(group_name)
            time.sleep(2)
            
            group_selector = f'//span[@title="{group_name}"]'
            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.XPATH, group_selector))
            )
            
            group = self.driver.find_element(By.XPATH, group_selector)
            group.click()
            time.sleep(2)
            
            message_box_selector = '//div[@contenteditable="true"][@data-testid="conversation-compose-box-input"]'
            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.XPATH, message_box_selector))
            )
            
            message_box = self.driver.find_element(By.XPATH, message_box_selector)
            message_box.clear()
            message_box.send_keys(message)
            
            send_button_selector = '//span[@data-testid="send"]'
            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.XPATH, send_button_selector))
            )
            
            send_button = self.driver.find_element(By.XPATH, send_button_selector)
            send_button.click()
            
            print(f"Mensaje enviado a {group_name}")
            return True
            
        except Exception as e:
            print(f"Error al enviar mensaje: {e}")
            return False
    
    def close(self):
        # Cerrar sesion
        if self.driver:
            self.driver.quit()
            print("Sesion cerrada")
