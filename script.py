from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Lista para almacenar distribuidores
distribuidores = []
opcion = input("Ingrese a donde desea ir: ").strip()
url = f"https://wega.com.ar/es/{opcion}/"
driver = webdriver.Chrome()
marcas_modelos = {}
valores = []
cont = 0
cont_marca = 0

try:
    if opcion == "distribuidores":
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "sucursal")))
        enlaces = driver.find_elements(By.ID, "sucursal")
        
        if enlaces:
            for enlace in enlaces:
                print(f"Nombre: {enlace.text}")
                distribuidores.append(enlace.text)
        else:
            print("No se encontraron distribuidores.")
    
    elif opcion == "catalogo":
        url_a_buscar2 = "https://wega.com.ar/es/catalogos/seccion/filtros"
        driver.get(url_a_buscar2)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "vehiculo")))
        
        # Obtener el elemento <select>
        vehiculos = driver.find_element(By.ID, "vehiculo")
        
        if vehiculos:
            print("Elemento encontrado.")
            select_categoria = Select(vehiculos) 
            select_categoria.select_by_value("1")  # Seleccionar "Auto"
            print("Categoría seleccionada:", select_categoria.first_selected_option.text)

            # Hacer clic en el botón para buscar marcas

            # Esperar a que las marcas se carguen
            marcas = driver.find_elements(By.ID, "marca-filtros")  # Ajustar el selector si es necesario

                
            if marcas:
                print("SE ACCEDIO A MARCAS")
                while cont_marca < len(marcas):  # Iterar sobre las marcas
                    marca = marcas[cont_marca]
                    marca_nombre = marca.text
                    print(f"ACCEDIENDO A: {marca.text}")
                    marca.click()
                    time.sleep(1)
                for marca in marcas:
                    marca_nombre = marca.text
                    print(f"ACCEDIENDO A: {marca.text}")
                    marca.click()
                    time.sleep(1)
                    
                    # Esperar a que los modelos se carguen
                    # Ajustar el selector si es necesario
                    modelos_select = Select(driver.find_element(By.ID, "modelo-filtros"))
                    
                    
                    if modelos_select.options:
                        print(f"Modelos disponibles para la marca {marca_nombre}:")
                        cont_modelo = 0  # Inicializar contador para modelos
                        while cont_modelo < len(modelos_select.options):  # Iterar sobre los modelos
                            option = modelos_select.options[cont_modelo]
                            value = option.get_attribute("value")  # Obtener el valor de la opción
                            text = option.text  # Obtener el texto de la opción

                            # Imprimir el valor y el texto
                            print(f"Modelo: {text}, Value: {value}")

                            # Seleccionar el modelo por su valor
                            modelos_select.select_by_value(value)
                            time.sleep(1)  # Esperar un momento después de la selección
                            cont_modelo += 1  # Incrementar el contador de modelos
                            
                            

                    time.sleep(1)
                   

            else:
                print("NO SE ENCONTRARON MARCAS ")
        else:
            print(f"NO SE ENCONTRO NADA EN {url_a_buscar2}")
except Exception as e:
    print("ERROR",e)

time.sleep(2)  # Esperar un momento para ver los resultados
 # Cerrar el navegador

driver.quit() 