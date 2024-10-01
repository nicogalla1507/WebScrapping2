from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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

    def fetch_marcas(self):
        marcas = self.driver.find_elements(By.ID, "marca-filtros")  
        
        if marcas:
            print("SE ACCEDIO A MARCAS")
            for marca in marcas:
                marca_nombre = marca.text.strip()  # Obtiene el nombre de la marca
                print(f"MARCA: {marca_nombre}") 
                

                 # Ajusta el selector según la estructura
        else:
            print("No se encontraron marcas.")        




    def fetch_modelos(self):
        indexx = []
        cont = 0
        
        # Espera hasta que el elemento <select> sea visible
        modelos = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "modelo-filtros"))
        )
        
        # Crea un objeto Select con el elemento encontrado
        var = Select(modelos)
        
        # Obtén el número total de opciones
        total_opciones = len(var.options)
        
        # Genera índices hasta 5000 o hasta que se acaben las opciones
        while cont < 5000 and cont < total_opciones:
            indexx.append(cont)
            cont += 1

        # Selecciona opciones por índice y las imprime
        for i in indexx:
            try:
                var.select_by_index(i)
                print(f"Seleccionado índice: {i}, Opción: {var.options[i].text}")
            except Exception as e:
                print(f"Error al seleccionar índice {i}: {e}")

        # Obtiene y muestra todas las opciones disponibles
        opciones = var.options
        if opciones:
            for modelo in opciones:
                time.sleep(1)  # Pausa de 1 segundo entre impresiones
                print(f"ACCEDIO: {modelo.text} - Value: {modelo.get_attribute('value')}")
        else:
            print("No hay opciones disponibles.")

           
    
    
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
            catalogo.select_categoria("1")  # Seleccionar "Auto"
            catalogo.fetch_marcas()
            catalogo.fetch_modelos()

    except Exception as e:
        print("ERROR", e)
    finally:
        time.sleep(2)
        web_driver_manager.quit()

if __name__ == "__main__":
    main()
