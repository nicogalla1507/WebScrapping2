            df_modelo = pd.DataFrame(especificaciones_totales)

                        # Guardamos en un archivo Excel
                        nombre_archivo = f"Autos.xlsx"
                        df_modelo.to_excel(nombre_archivo, index=False)
                        print(f"Guardado: {nombre_archivo}")