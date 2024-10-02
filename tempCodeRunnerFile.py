        codigos = self.driver.find_elements(By.CLASS_NAME, "title-dark")
        titulos = []
        largo_codigos = len(codigos)
        print(codigos.text)