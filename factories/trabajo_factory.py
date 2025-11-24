class TrabajoFactory:
    @staticmethod
    def crear_configuracion(tipo_trabajo):
        if not tipo_trabajo:
            return None
            
        tipo = tipo_trabajo.lower().strip()
        
       
        if tipo == "tesis":
            return {
                "tipo_db": "Tesis de Grado", # Esto se ignora si usas una tabla de tipos, pero sirve de referencia
                "duracion_meses": 12,
                "nota_aprobacion": 4.0,
                "requisito": "Investigación + Paper Académico"
            }
        elif tipo == "proyecto":
            return {
                "tipo_db": "Proyecto de Título",
                "duracion_meses": 6,
                "nota_aprobacion": 4.0,
                "requisito": "Software Funcional + Documentación"
            }
        elif tipo == "seminario":
            return {
                "tipo_db": "Seminario",
                "duracion_meses": 4,
                "nota_aprobacion": 5.0, # Ejemplo: Seminario exige más nota
                "requisito": "Informe Técnico"
            }
        else:
            return None