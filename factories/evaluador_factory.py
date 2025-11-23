class EvaluadorFactory:
    """
    Fábrica que define los roles de los profesores.
    """
    @staticmethod
    def crear_perfil(tipo_evaluador):
        tipo = tipo_evaluador.lower().strip()

        if tipo == "guia":
            return {
                "tipo": "Profesor Guía",
                "rol": "Supervisor Principal",
                "permisos": "total"
            }
        elif tipo == "comision":
            return {
                "tipo": "Comisión Evaluadora",
                "rol": "Evaluador Externo",
                "permisos": "lectura_nota"
            }
        elif tipo == "informante":
            return {
                "tipo": "Profesor Informante",
                "rol": "Revisor Técnico",
                "permisos": "lectura"
            }
        else:
            return None