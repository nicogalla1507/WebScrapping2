    def aplicaciones(self):
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

                            buscar_button = self.driver.find_element(By.ID, "buscarTipo-filtros")
                            buscar_button.click()

                            time.sleep(2)  # Espera para que carguen los datos

                            # Extraer los detalles de la página de productos
                            img_wrappers = self.driver.find_elements(By.CLASS_NAME, "img-wrapper")

                            for i, img_wrapper in enumerate(img_wrappers):
                                try:
                                    img_wrappers = self.driver.find_elements(By.CLASS_NAME, "img-wrapper")
                                    img_wrapper = img_wrappers[i]

                                    link_img_wrapper = img_wrapper.find_element(By.TAG_NAME, 'a')
                                    link_img_wrapper.click()

                                    # Capturar título y código
                                    titulo = self.driver.find_element(By.CLASS_NAME, "title")
                                    codigo = self.driver.find_element(By.XPATH, "/html/body/section[1]/div[3]/div/div[5]/h2")

                                    # Capturar la lista de aplicaciones, usando saltos de línea '\n'
                                    aplicaciones_section = self.driver.find_element(By.CLASS_NAME, "aplicaciones")
                                    aplicaciones_spans = aplicaciones_section.find_elements(By.CLASS_NAME, "content-hidden")
                                    
                                    # Extraer cada aplicación y unirlas con saltos de línea
                                    aplicaciones_texto = "\n".join([app.text.strip() for app in aplicaciones_spans])

                                    # Capturar equivalencias si existen
                                    equivalencias = self.driver.find_elements(By.CLASS_NAME, "block-table")
                                    lista_eq = []

                                    if equivalencias:
                                        for equivalencia in equivalencias:
                                            eq_texto = equivalencia.text.strip()
                                            strong_elements = equivalencia.find_elements(By.TAG_NAME, 'strong')
                                            if strong_elements:
                                                eq_texto_strong = ' '.join([strong.text.strip() for strong in strong_elements])
                                                eq_texto += f" {eq_texto_strong}"
                                            lista_eq.append(eq_texto)

                                    especificaciones = {
                                        'Codigo': codigo.text.strip(),
                                        "Aplicaciones": aplicaciones_texto,
                                        "Equivalencias": lista_eq,
                                        "Tipo": titulo.text.strip()
                                    }

                                    especificaciones_totales.append(especificaciones)

                                    # Guardar en Excel después de cada extracción
                                    df = pd.DataFrame(especificaciones_totales)
                                    df.to_excel('especificaciones_modelo_completas.xlsx', index=False)
                                    print("GUARDADO")

                                    self.driver.back()
                                    marca = self.driver.find_element(By.XPATH, marca_xpath)
                                    marca.click()
                                    modelos = self.driver.find_elements(By.XPATH, "//select[@id='modelo-filtros']/option")
                                    modelo = self.driver.find_element(By.XPATH, modelo_xpath)
                                    modelo.click()

                                except NoSuchElementException as e:
                                    print("ERROR", e)

        except NoSuchElementException as e:
            print(f"Error: {e}")