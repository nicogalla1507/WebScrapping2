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
                for marca in marcas:
                    
                    print(f"ACCEDIENDO A: {marca.text}")
                    time.sleep(1)
                    
                    # Esperar a que los modelos se carguen
                    modelos = driver.find_elements(By.ID,"modelo-filtros")  # Ajustar el selector si es necesario
                    
                    if modelos:
                        print("Modelos encontrados:")
                        for modelo in modelos:
                            time.sleep(1)
                            print(f"ACCEDIENDO A: {modelo.text}")
                    else:
                        print("NO SE ENCONTRARON MODELOS ")
                    
                    driver.back()  # Volver a la página anterior para seleccionar otra marca
                    time.sleep(1)  # Esperar un segundo antes de continuar
                    # Esperar a que la página de marcas se recargue
                    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "marca-filtros")))

            else:
                print("NO SE ENCONTRARON MARCAS ")
        else:
            print(f"NO SE ENCONTRO NADA EN {url_a_buscar2}")

finally:
    time.sleep(2)  # Esperar un momento para ver los resultados
    driver.quit()  # Cerrar el navegador
