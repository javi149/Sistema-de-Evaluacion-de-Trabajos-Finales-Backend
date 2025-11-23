class TrabajoFactory:
    """
    Fábrica que define las reglas de negocio para Tesis, Proyectos y Seminarios.
    """
    @staticmethod
    def crear_configuracion(tipo_trabajo):
        tipo = tipo_trabajo.lower().strip()
        
        if tipo == "tesis":
            return {
                "tipo_db": "Tesis de Grado",
                "duracion_meses": 12,
                "nota_aprobacion": 4.0,
                "requisito": "Investigación Bibliográfica"
            }
        elif tipo == "proyecto":
            return {
                "tipo_db": "Proyecto de Título",
                "duracion_meses": 6,
                "nota_aprobacion": 4.0,
                "requisito": "Software Funcional"
            }
        elif tipo == "seminario":
            return {
                "tipo_db": "Seminario de Título",
                "duracion_meses": 4,
                "nota_aprobacion": 4.0,
                "requisito": "Informe Técnico"
            }
        else:
            return None