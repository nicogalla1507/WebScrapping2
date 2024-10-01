from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random


class WebDriverManager:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome()

    def open(self):
        self.driver.get(self.url)

    def quit(self):
        self.driver.quit()

class Distribuidores:
    def __init__(self, driver):
        self.driver = driver
        self.distribuidores = []

    def fetch_distribuidores(self):

        enlaces = self.driver.find_elements(By.ID, "sucursal")
        
        if enlaces:
            for enlace in enlaces:
                print(f"Nombre: {enlace.text}")
                self.distribuidores.append(enlace.text)
        else:
            print("No se encontraron distribuidores.")
        
class Catalogo:
    def __init__(self, driver):
        self.driver = driver
        self.diccionario = {}
        
    def select_categoria(self, value):
        vehiculos = self.driver.find_element(By.ID, "vehiculo")
        select_categoria = Select(vehiculos) 
        select_categoria.select_by_value(value)
        print("Categoría seleccionada:", select_categoria.first_selected_option.text)


    def fetch_modelos_marca(self):
        try:

            sel_marcas = self.driver.find_element(By.ID, "marca-filtros")
            seleccionar_marca = Select(sel_marcas)


            for marca in seleccionar_marca.options:
                print(f"Seleccionando Marca: {marca.text}")
                seleccionar_marca.select_by_visible_text(marca.text)
                time.sleep(2)  


                sel_modelos = self.driver.find_element(By.ID, "modelo-filtros")
                seleccionar_modelo = Select(sel_modelos)


                for modelo in seleccionar_modelo.options:

                    print(f"Modelo para {marca.text}: {modelo.text}")
                    boton = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "buscarTipo-filtros")))
                    boton.click()
                    specs = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "js-intercambiable-th")))
                    for s in specs:
                        print(f"Especificacion de {modelo.text} {s.text}")
                time.sleep(2)


        except Exception as e:
            print(f"Ocurrió un error: {str(e)}")

        
    def buscar_codigo(self):
        pass

def main():
    opcion = input("Ingrese a donde desea ir: ").strip()
    url = f"https://wega.com.ar/es/{opcion}/"
    
    web_driver_manager = WebDriverManager(url)
    
    try:
        web_driver_manager.open()
        
        if opcion == "distribuidores":
            distribuidores = Distribuidores(web_driver_manager.driver)
            distribuidores.fetch_distribuidores()
        
        elif opcion == "catalogo":
            url_catalogo = "https://wega.com.ar/es/catalogos/seccion/filtros"
            web_driver_manager.driver.get(url_catalogo)
            WebDriverWait(web_driver_manager.driver, 10).until(EC.presence_of_element_located((By.ID, "vehiculo")))
            
            catalogo = Catalogo(web_driver_manager.driver)
            catalogo.select_categoria("1")
            time.sleep(2)
            catalogo.fetch_modelos_marca()


    except Exception as e:
        print("ERROR", e)
    finally:
        time.sleep(2)
        web_driver_manager.quit()

if __name__ == "__main__":
    main()
