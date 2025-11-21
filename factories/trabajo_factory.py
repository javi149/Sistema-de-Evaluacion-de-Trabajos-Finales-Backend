class TrabajoFactory:
    """
    Fábrica que recibe un TIPO de trabajo (string)
    y devuelve un DICCIONARIO con la configuración académica.
    """
    
    @staticmethod
    def crear_configuracion(tipo_trabajo):
        # 1. Limpiamos el texto (minusculas y sin espacios)
        tipo = tipo_trabajo.lower().strip()
        
        # 2. Lógica de Negocio: Definir reglas según el tipo
        if tipo == "tesis":
            return {
                "tipo_db": "Tesis de Grado",
                "duracion_meses": 12,        # Regla: Tesis dura 1 año
                "nota_aprobacion": 4.0,      # Regla: Se aprueba con 4.0
                "requisito": "Investigación Bibliográfica"
            }
            
        elif tipo == "proyecto":
            return {
                "tipo_db": "Proyecto de Título",
                "duracion_meses": 6,         # Regla: Proyecto dura 1 semestre
                "nota_aprobacion": 4.0,      # Regla: Proyecto exige más nota
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
            # Retornamos None si escriben cualquier cosa
            return None