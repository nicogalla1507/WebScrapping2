from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup


class WebDriverManager:
    def __init__(self, url):
        options = webdriver.ChromeOptions() 
        self.url = url
        self.driver = webdriver.Chrome(options=options)

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

                    if seleccionar_modelo.options:
                       for _ in range(3): 
                            try:

                                boton = self.driver.find_element(By.ID, "buscarTipo-filtros")
                                if boton.is_displayed() and boton.is_enabled():
                                    boton.click()
                                    print(f"Botón de buscar clicado para {marca.text} - {modelo.text}")

                                    
                                    time.sleep(5)  

                                    
                                    specs = self.driver.find_elements(By.CLASS_NAME, "js-intercambiable-th")
                                    if specs:
                                        print(f"Especificaciones cargadas para {marca.text} - {modelo.text}:")
                                        for spec in specs:
                                            print(spec.text)
                                    else:
                                        print("No se encontraron especificaciones.")
                                for spec in specs:
                                    print(spec.text)

                                break  
                            except Exception as e:
                                print("error",type(e))
                    specs_motor = self.driver.find_elements(By.LINK_TEXT, "Motor")
                    specs_anio = self.driver.find_elements(By.LINK_TEXT, "Año")
                    specs_aire = self.driver.find_elements(By.LINK_TEXT, "Aire")
                    specs_aceite = self.driver.find_elements(By.LINK_TEXT, "Aceite")
                    specs_combustible = self.driver.find_elements(By.LINK_TEXT,"Combustible")
                    specs_hab = self.driver.find_elements(By.LINK_TEXT,"Habitáculo")
                    print("SE ENCONTROOO")
                    print(f"Especificaciones cargadas para {marca.text} - {modelo.text}:")


        except Exception as e:
            print(f"Ocurrió un error: {str(e)}")
class CatalogoPiezas:
    def __init__(self, driver):
        self.driver = driver

    def open(self, url):
        self.driver.get(url)
        
    def select_categoria(self):
        
        todos_los_codigos = []
        codigos = self.driver.find_elements(By.CLASS_NAME, "title-dark")
        titulos = []


        for cod in codigos:
            cod_texto= cod.text.strip()
            print(cod_texto)
            title_element = self.driver.find_element(By.XPATH, f"//h2[contains(@class, 'title-dark') and text()='{cod_texto}']")
            parent_div = title_element.find_element(By.XPATH, "./ancestor::div[@class='row']")
            ver_mas_button = parent_div.find_element(By.XPATH, ".//a[contains(text(), 'Ver más')]")
            titulos.append(title_element.text)
            try:
                codigos

                #boton.click()
                ver_mas_button.click()
                time.sleep(2)  

                aplicacion = self.driver.find_element(By.TAG_NAME, "h3").text
                specs = self.driver.find_element(By.CLASS_NAME, "aplicaciones").text
                if specs:
                    boton2 = self.driver.find_element(By.ID,"vermas2")
                    boton2.click()
                    time.sleep(2)
                self.driver.back()

                todos_los_codigos.append({
                    'aplicacion': aplicacion,
                    'especificaciones': specs
                })

                print(f" Aplicación: {aplicacion}, Especificaciones: {specs}")

                # Hacer clic en el botón 'Ver más' si está presente
                try:
                    

                    # Extraer especificaciones expandidas
                    
                    print(f"Especificaciones expandida: {specs}")

                    # Volver a la página anterior
                    
                    time.sleep(2)

                except Exception as e:
                    print(f"No se encontró el botón 'Ver más': {e}")
                    self.driver.back()
                    time.sleep(2)

                # Volver a obtener los códigos después de regresar

                  # Salir del bucle para comenzar de nuevo

            except Exception as e:
                print(f"Ocurrió un error al procesar el código: {e}")
                self.driver.back()  # Volver a la página anterior en caso de error
                time.sleep(2)
                    
        # Mostrar todos los códigos extraídos
        for idx, codigo in enumerate(todos_los_codigos, 1):
            print(f"CÓDIGO {idx}: {codigo}")
        return todos_los_codigos
                
              

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
            time.sleep(2)  
            
            catalogo = Catalogo(web_driver_manager.driver)
            catalogo.select_categoria("1")
            catalogo.fetch_modelos_marca()
        
        elif opcion == "piezas":
            url_piezas = "https://wega.com.ar/es/fichas_filtros_habitaculos"
            piezas = CatalogoPiezas(web_driver_manager.driver)
            piezas.open(url_piezas)
            piezas.select_categoria()
            
    except Exception as e:
        print("ERROR:", e)
    finally:
        if web_driver_manager.driver:
            time.sleep(2)
            web_driver_manager.quit()

if __name__ == "__main__":
    main()
