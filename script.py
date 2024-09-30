from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC






#Lista para almacenar distribuidores
distribuidores = []
opcion = input("Ingrese a donde desea ir: ").strip()
url = f"https://wega.com.ar/es/{opcion}/"
driver = webdriver.Chrome()
url_a_buscar = url

if opcion == "distribuidores":
    driver.get(url_a_buscar)
    enlaces = driver.find_elements(By.ID,"sucursal")
    if enlaces:
        for enlace in enlaces:
            print(f"Nombre: {enlace.text}")
elif opcion == "catalogo":
    url_a_buscar2 = "https://wega.com.ar/es/catalogos/seccion/filtros"
    driver.get(url_a_buscar2)
    catalogo = driver.find_elements(By.ID,"vehiculo")
    for catalogos in catalogo:
        print(catalogos.text)
    if catalogo:
        op = input("INGRESE A QUE CATEGORIA DE VEHICULO DESEA INGRESAR (A)auto (c)Camiones (M)motos").upper()
        if op == "A":
            categoria = Select(catalogo)
            categoria.select_by_visible_text("Autos")
            if categoria is not None:
                print(categoria)

            else:
                print("ERROR")
        else:
            print("NO SE ENCONTRARON AUTOS")
        #buscar catalogo de autos
        print("SE ENCONTRARON",len(catalogo),"elementos")
    else:
        print(f"NO SE ENCONTRO NADA EN {catalogo} ")
    
    


driver.close()