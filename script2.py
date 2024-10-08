from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
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

                    
                    try:
                        marca.click()
                    except Exception as e:
                        print(f"Error al hacer clic en la marca: {e}")
                        continue  
                   
                    time.sleep(2)

                    modelos = self.driver.find_elements(By.XPATH, "//select[@id='modelo-filtros']/option")

                    for contador_modelo in range(1, len(modelos) + 1):
                    
                        modelo_xpath = f"(//select[@id='modelo-filtros']/option)[{contador_modelo}]"
                        modelo = self.driver.find_element(By.XPATH, modelo_xpath)
                        valor_modelo = modelo.get_attribute('value')
                        texto_modelo = modelo.text.strip()

                        if valor_modelo:
                            print(f"Seleccionando Modelo: {texto_modelo}, Valor: {valor_modelo}")
                            modelo.click()

                            
                
                            buscar_button = self.driver.find_element(By.ID, "buscarTipo-filtros")
                            buscar_button.click()
                            btn= self.driver.find_elements(By.CLASS_NAME,"img-wrapper")
                            for b in btn:
                                try:
                                    # Obtener el atributo href del botón/enlace
                                    href = b.get_attribute('href')
                                    print(f"Enlace encontrado: {href}")

                                    # Hacer clic en el enlace
                                    b.click()
                                    time.sleep(2)  # Pausa para cargar la página o hacer alguna acción necesaria

                                    # Aquí puedes agregar la lógica para buscar aplicaciones u otros elementos dentro de la nueva página
                                    # Por ejemplo:
                                    aplicaciones = self.driver.find_elements(By.TAG_NAME, 'br')
                                    for aplicacion in aplicaciones:
                                        print(aplicacion.text)

                                    # Volver a la página original (si es necesario)
                                    self.driver.back() 
                                except NoSuchElementException:
                                    print("ERROR")
                            
                            
                            specs = self.driver.find_elements(By.TAG_NAME, "td")
                            
                            modelos = self.driver.find_elements(By.XPATH, "//select[@id='modelo-filtros']/option")
                            especificaciones_modelo = {
                                "Marca": texto_marca,
                                "Modelo": texto_modelo,
                                "Motor": '',          
                                "Año": '',            
                                "Aire": '',           
                                "Aceite": '',         
                                "Combustible": '',    
                                "Habitáculo": ''      
                            }
                            for campo in ['Motor', 'Año', 'Aire', 'Aceite', 'Combustible', 'Habitáculo']:
                                try:
                                    td_element = self.driver.find_element(By.XPATH, f"//td[@data-title='{campo}']")
                                    especificaciones_modelo[campo] = td_element.text.strip()
                                except NoSuchElementException:
                                    especificaciones_modelo[campo] = 'No disponible'

                                especificaciones_totales.append(especificaciones_modelo)
                                print(f"Especificaciones agregadas: {especificaciones_modelo}")
                                    
                                especificaciones_totales.append(especificaciones_modelo)
                                print(f"Especificaciones agregadas: {especificaciones_modelo}")
                        
                    df_modelo = pd.DataFrame(especificaciones_totales)

                    
                    nombre_archivo = f"Autos.xlsx"
                    excel = df_modelo.to_excel(nombre_archivo, index=False)
                    print(f"Guardado: {nombre_archivo}")
                    
                             
                    

        except NoSuchElementException as e:
            print("ERROR =>", e)
    def aplicaciones(self):
        marcas = self.driver.find_elements(By.XPATH, "//select[@id='marca-filtros']/option")
        aplicaciones_totales = []  # Inicializa la lista de aplicaciones totales

        try:
            for contador_marca in range(1, len(marcas) + 1):
                marca_xpath = f"(//select[@id='marca-filtros']/option)[{contador_marca}]"
                marca = self.driver.find_element(By.XPATH, marca_xpath)
                valor_marca = marca.get_attribute('value')
                texto_marca = marca.text.strip()

                if valor_marca:
                    print(f"Contador: {contador_marca}, Marca: {texto_marca}, Valor: {valor_marca}")

                    try:
                        marca.click()
                    except Exception as e:
                        print(f"Error al hacer clic en la marca: {e}")
                        continue  

                    time.sleep(2)

                    modelos = self.driver.find_elements(By.XPATH, "//select[@id='modelo-filtros']/option")

                    for contador_modelo in range(1, len(modelos) + 1):
                        modelo_xpath = f"(//select[@id='modelo-filtros']/option)[{contador_modelo}]"
                        modelo = self.driver.find_element(By.XPATH, modelo_xpath)
                        valor_modelo = modelo.get_attribute('value')
                        texto_modelo = modelo.text.strip()

                        if valor_modelo:
                            print(f"Seleccionando Modelo: {texto_modelo}, Valor: {valor_modelo}")
                            modelo.click()

                            buscar_button = self.driver.find_element(By.ID, "buscarTipo-filtros")
                            buscar_button.click()

                            campos = ['Aire', 'Aceite', 'Combustible', 'Habitáculo']
                            contador_campo = 0
                            img_wrappers = self.driver.find_elements(By.CLASS_NAME,"img-wrapper")
                            while True:
                            # Obtener todos los img-wrapper de la página actual
                                img_wrappers = self.driver.find_elements(By.CLASS_NAME, "img-wrapper")
                                
                                if not img_wrappers:
                                    print("No hay más img-wrapper en la página.")
                                    break

                                for i, img_wrapper in enumerate(img_wrappers):
                                    try:
                                        # Re-localizar el img-wrapper antes de cada clic para evitar problemas con DOM recargado
                                        img_wrappers = self.driver.find_elements(By.CLASS_NAME, "img-wrapper")
                                        img_wrapper = img_wrappers[i]
                                        link_img_wrapper = img_wrapper.find_element(By.TAG_NAME, 'a')
                                        link_img_wrapper.click()

                                        time.sleep(2)

                                        # Obtener aplicaciones en la página
                                        aplicaciones = self.driver.find_elements(By.TAG_NAME, 'br')
                                        aplicaciones_texto = [aplicacion.text.strip() for aplicacion in aplicaciones]

                                        aplicaciones_totales.append({
                                            "Aplicaciones": aplicaciones_texto
                                        })

                                        self.driver.back()
                                        time.sleep(2)

                                    except NoSuchElementException:
                                        print(f"No se encontró el enlace en img-wrapper para la iteración {i}.")

                                # Intentar navegar a la siguiente página
                                try:
                                    siguiente_pagina = WebDriverWait(self.driver, 10).until(
                                        EC.visibility_of_element_located((By.XPATH, "//a[contains(text(), 'Siguiente')]"))
                                    )
                                    siguiente_pagina.click()
                                    time.sleep(2)  # Esperar a que la nueva página se cargue

                                except TimeoutException:
                                    print("No se encontró el botón de 'Siguiente' o no está visible, terminando la búsqueda.")
                                    break  # Salir del bucle si no hay más páginas

        except NoSuchElementException as e:
            print("ERROR", e)

        # Al final, puedes guardar o procesar aplicaciones_totales como desees
        print("Aplicaciones totales encontradas:", aplicaciones_totales)

            
            
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
        nombre2 = ""  

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
            
            autos = catalogo.select_categoria("1")
            catalogo.aplicaciones()
            catalogo.fetch_modelos_marca()
            if autos:
                camiones = catalogo.select_categoria("3")
                catalogo.fetch_modelos_marca()
                if camiones:
                    motos = catalogo.select_categoria("4")
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