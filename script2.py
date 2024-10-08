from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from selenium.common.exceptions import NoSuchElementException
import pandas as pd


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
        especificaciones_totales = []
        marcas = self.driver.find_elements(By.XPATH, "//select[@id='marca-filtros']/option")
        try: 
            for contador_marca in range(1, len(marcas) + 1):
        
                marca_xpath = f"(//select[@id='marca-filtros']/option)[{contador_marca}]"
                marca = self.driver.find_element(By.XPATH, marca_xpath)
                valor_marca = marca.get_attribute('value')
                texto_marca = marca.text.strip()

                if valor_marca:
                    print(f"Contador: {contador_marca}, Marca: {texto_marca}, Valor: {valor_marca}")
                    marca.click()  
                    time.sleep(1)  

                    
                    modelos = self.driver.find_elements(By.XPATH, "//select[@id='modelo-filtros']/option")
                    
                    for contador_modelo in range(1, len(modelos) + 1):
                        
                        modelo_xpath = f"(//select[@id='modelo-filtros']/option)[{contador_modelo}]"
                        modelo = self.driver.find_element(By.XPATH, modelo_xpath)
                        valor_modelo = modelo.get_attribute('value')
                        texto_modelo = modelo.text.strip()

                        if valor_modelo:
                            print(f"Seleccionando Modelo: {texto_modelo}, Valor: {valor_modelo}")
                            
                            
                            modelo.click()
                            time.sleep(1)  

                            
                            buscar_button = self.driver.find_element(By.ID, "buscarTipo-filtros")
                            buscar_button.click()

                        
                            time.sleep(2)
                            specs = self.driver.find_elements(By.TAG_NAME, "td")
                            self.driver.back()
        
                            time.sleep(1)  
                            
        except NoSuchElementException as e:
            print("ERROR =>",e)
                # Crear un DataFrame después de procesar todos los modelos de la marca
            


                    
                
                    
                
            
            
            
class CatalogoPiezas:
    def __init__(self, driver):
        self.driver = driver

    def open(self, url):
        self.driver.get(url)
        
    def select_categoria(self):
        
        todos_los_codigos = []
        codigos = self.driver.find_elements(By.CLASS_NAME, "title-dark")
        titulos = [c.text.strip() for c in codigos]  # Recoge los títulos
        print(titulos)
        
        cont = 0
        cont_pagina = 1
        nombre2 = ""  # Inicializa nombre2 para evitar el error

        while cont < 10:
            try:
                if cont_pagina == 1:
                    nombre = titulos[cont]
                else:
                    nombre = titulos2[cont]

                title_element = self.driver.find_element(By.XPATH, f"//h2[contains(@class, 'title-dark') and text()='{nombre}']")
                

                parent_div = title_element.find_element(By.XPATH, "./ancestor::div[@class='row']")
                ver_mas_button = parent_div.find_element(By.XPATH, ".//a[contains(text(), 'Ver más')]")
                

                ver_mas_button.click()
                
                enlace_imagen = self.driver.find_element(By.XPATH,"/html/body/section[1]/div[3]/div/div[4]/img")
                src = enlace_imagen.get_attribute('src')

                
                aplicacion = self.driver.find_element(By.TAG_NAME, "h3").text
                specs = self.driver.find_element(By.CLASS_NAME, "aplicaciones").text
                print(f"Aplicación: {aplicacion}, Especificaciones: {specs}")

                if specs:

                    try:
                        boton2 = self.driver.find_element(By.ID, "vermas2")
                        boton2.click()

                        equivalencias = self.driver.find_elements(By.CLASS_NAME, "block-table")
                        if equivalencias:
                            lista_eq = [e.text.strip() for e in equivalencias]
                            print(lista_eq)

                        boton3 = self.driver.find_element(By.ID, "vermas-eq")
                        boton3.click()
                        
                        lista_dimensiones = []
                        for i in range(1,11):
                            dimensiones = self.driver.find_element(By.XPATH, f"//*[@id='dimensiones']/div/table/tbody/tr[2]/td[{i}]").text
                            lista_dimensiones.append(dimensiones)
                    except NoSuchElementException:
                        print("No se encontró el botón para expandir más detalles.")
                

                self.driver.back()

                #//*[@id="dimensiones"]/div/table/tbody/tr[2]/td[1]
                
                todos_los_codigos.append({
                    'CODIGO': nombre,
                    'APLICACION': aplicacion,
                    'ESPECIFICACIONES': specs,
                    'DIMENSIONES': lista_dimensiones,
                    'URL IMAGEN': src
                })
                cont += 1


                if cont == 10:
                    cont = 0
                    cont_pagina += 1
                    titulos2 = []
                    try:
                        boton_paginador = self.driver.find_element(By.XPATH, f"//*[@id='paginador']/nav/ul/li[{cont_pagina}]/a")
                        boton_paginador.click()
                        codigos = self.driver.find_elements(By.CLASS_NAME, "title-dark")
                        for c in codigos:
                            titulos2.append(c.text.strip()) 
                        nombre2 = titulos2[cont]  
                        print(f"Procesando el producto {cont+1}: {nombre2}")
                    except NoSuchElementException:
                        print("No se encontró el botón de paginación o se llegó al final.")
                        break
            except NoSuchElementException as e:
                print(f"Error al procesar el producto: {e}")
                break
            except Exception as e:
                print(f"Ocurrió un error: {e}")
                self.driver.back()
        df = pd.DataFrame(todos_los_codigos,columns=["CODIGO","APLICACION","ESPECIFICACIONES","DIMENSIONES","URL IMAGEN"])
        df.to_excel('Datos.xlsx',index=False)
        print("DATOS EXPORTADOS")
        

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