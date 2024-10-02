    def select_categoria(self):
        cont = 0
        todos_los_codigos = []  # Lista para almacenar todos los códigos encontrados

        # Encuentra todos los códigos disponibles en la página inicial
        codigos = self.driver.find_elements(By.CLASS_NAME, "title-dark")

        while cont < len(codigos):  # Itera sobre todos los códigos encontrados
            try:
                # Encuentra y haz clic en el botón "Ver más" del código actual
                boton = codigos[cont].find_element(By.CLASS_NAME, "more")  # Busca el botón en el elemento actual
                boton.click()  # Haz clic en el botón "Ver más"
                time.sleep(2)  # Espera a que la página de detalles cargue

                # Extrae la información adicional (ajusta el selector si es necesario)
                specs = self.driver.find_element(By.CLASS_NAME, "content-hidden")
                todos_los_codigos.append(specs.text)  # Almacena las especificaciones
                print(specs.text)  # Imprime las especificaciones

                # Busca y haz clic en el segundo botón "Ver más" si existe
                try:
                    boton2 = self.driver.find_element(By.ID, "vermas2")
                    boton2.click()
                    time.sleep(2)  # Espera un momento para que cargue la nueva información

                    # Extrae las aplicaciones si el segundo botón fue encontrado
                    specs_aplicaciones = self.driver.find_element(By.CLASS_NAME, "aplicaciones")
                    todos_los_codigos.append(specs_aplicaciones.text)
                    print(specs_aplicaciones.text)  # Imprime las aplicaciones

                except Exception as e:
                    print(f"No se encontró el segundo botón 'Ver más': {e}")

                # Vuelve a la página anterior (lista de códigos)
                self.driver.back()
                time.sleep(2)  # Espera a que la página de códigos cargue nuevamente

                # Vuelve a encontrar los códigos ya que la página se ha recargado
                codigos = self.driver.find_elements(By.CLASS_NAME, "title-dark")
                cont += 1  # Incrementa el contador para pasar al siguiente código

            except Exception as e:
                print(f"Ocurrió un error: {e}")
                self.driver.back()  # Asegúrate de volver a la página de códigos si hay un error
                time.sleep(2)

                # Refresca la lista de códigos para continuar con el siguiente
                codigos = self.driver.find_elements(By.CLASS_NAME, "title-dark")
                # No incrementes el contador aquí, ya que quieres volver a procesar el mismo código
                continue

        # Imprime todos los códigos encontrados con sus especificaciones
        for idx, c in enumerate(todos_los_codigos, 1):
            print(f"CÓDIGO {idx}: {c}")