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

                    # Intentar hacer clic en la marca
                    try:
                        marca.click()
                    except Exception as e:
                        print(f"Error al hacer clic en la marca: {e}")
                        continue  # Pasar a la siguiente marca si no se puede hacer clic

                    # Esperar un momento para que se carguen los modelos
                    time.sleep(2)

                    modelos = self.driver.find_elements(By.XPATH, "//select[@id='modelo-filtros']/option")

                    for contador_modelo in range(1, len(modelos) + 1):
                        try:
                            modelo_xpath = f"(//select[@id='modelo-filtros']/option)[{contador_modelo}]"
                            modelo = self.driver.find_element(By.XPATH, modelo_xpath)
                            valor_modelo = modelo.get_attribute('value')
                            texto_modelo = modelo.text.strip()

                            if valor_modelo:
                                print(f"Seleccionando Modelo: {texto_modelo}, Valor: {valor_modelo}")
                                modelo.click()

                                # Esperar un momento para que el botón de buscar esté disponible
                                time.sleep(2)
                                buscar_button = self.driver.find_element(By.ID, "buscarTipo-filtros")
                                buscar_button.click()

                                # Esperar que las especificaciones se carguen
                                time.sleep(2)
                                specs = self.driver.find_elements(By.TAG_NAME, "td")

                                # Aquí podrías agregar lógica para procesar las especificaciones
                                for spec in specs:
                                    especificaciones_totales.append(spec.text.strip())

                                # Regresar a la página anterior (modelos)
                                self.driver.back()

                                # Esperar que la página anterior se cargue
                                time.sleep(2)

                                # No hacer clic de nuevo en la marca, ya que debe permanecer activa
                                # Volver a cargar los modelos
                                time.sleep(2)
                                modelos = self.driver.find_elements(By.XPATH, "//select[@id='modelo-filtros']/option")

                        except StaleElementReferenceException:
                            print(f"El modelo {contador_modelo} ya no es válido, intentando nuevamente.")
                            # Reintentar buscando nuevamente los modelos
                            modelos = self.driver.find_elements(By.XPATH, "//select[@id='modelo-filtros']/option")
                            modelo_xpath = f"(//select[@id='modelo-filtros']/option)[{contador_modelo}]"
                            modelo = self.driver.find_element(By.XPATH, modelo_xpath)
                            valor_modelo = modelo.get_attribute('value')
                            texto_modelo = modelo.text.strip()

                            if valor_modelo:
                                print(f"Seleccionando Modelo: {texto_modelo}, Valor: {valor_modelo}")
                                modelo.click()

                                # Esperar un momento para que el botón de buscar esté disponible
                                time.sleep(2)
                                buscar_button = self.driver.find_element(By.ID, "buscarTipo-filtros")
                                buscar_button.click()

                                # Esperar que las especificaciones se carguen
                                time.sleep(2)
                                specs = self.driver.find_elements(By.TAG_NAME, "td")

                                # Aquí podrías agregar lógica para procesar las especificaciones
                                for spec in specs:
                                    especificaciones_totales.append(spec.text.strip())

        except NoSuchElementException as e:
            print("ERROR =>", e)

        # Crear un DataFrame después de procesar todos los modelos de la marca
        # Por ejemplo, usando pandas:
        # df = pd.DataFrame(especificaciones_totales)
