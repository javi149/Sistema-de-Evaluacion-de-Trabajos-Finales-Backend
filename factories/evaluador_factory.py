class EvaluadorFactory:
    @staticmethod
    def crear_perfil(tipo_evaluador):
        if not tipo_evaluador:
            return None
            
        tipo = tipo_evaluador.lower().strip()

        if tipo == "guia":
            return {
                "tipo_oficial": "Profesor Guía",
                "rol": "Supervisor",
                "permisos": "total" # Puede editar notas
            }
        elif tipo == "comision":
            return {
                "tipo_oficial": "Comisión Evaluadora",
                "rol": "Evaluador Externo",
                "permisos": "lectura_escritura_nota"
            }
        elif tipo == "informante":
            return {
                "tipo_oficial": "Profesor Informante",
                "rol": "Revisor",
                "permisos": "lectura"
            }
        else:
            return None