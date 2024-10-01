for modelo in opciones:
            time.sleep(1)  # Pausa de 1 segundo entre impresiones
            print(f"ACCEDIO: {modelo.text} - Value: {modelo.get_attribute(indexx)}")
