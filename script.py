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
        catalogo = driver.find_element(By.ID, "vehiculo")  # Asegúrate de que esto sea correcto
        
        if catalogo:
            print("Elemento encontrado.")
            select_categoria = Select(catalogo)  # Crear objeto Select
            
            # Seleccionar por value
            select_categoria.select_by_value("1")  # "1" corresponde a "Auto"
            print("Categoría seleccionada:", select_categoria.first_selected_option.text)
            #AHORA LAS MARCAS
        else:
            print(f"NO SE ENCONTRO NADA EN {url_a_buscar2}")
    
finally:
    time.sleep(2)  # Esperar un momento para ver los resultados
    driver.quit()  # Cerrar el navegador
