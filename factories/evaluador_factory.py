class EvaluadorFactory:
    """
    Factory que recibe el TIPO de profesor (guia, informante)
    y devuelve sus permisos y cuánto vale su nota.
    """
    
    @staticmethod
    def crear_perfil(tipo_profe):
        tipo = tipo_profe.lower().strip()
        
        if "guia" in tipo:
            return {
                "rol_asignado": "Profesor Guía",
                "peso_voto": 0.60,  # El guía decide el 60% de la nota final
                "descripcion": "Responsable principal del alumno."
            }
        
        elif "informante" in tipo or "comision" in tipo:
            return {
                "rol_asignado": "Comisión Evaluadora",
                "peso_voto": 0.40,  # La comisión decide el 40%
                "descripcion": "Revisa el documento y evalúa la defensa."
            }
            
        else:
            # Caso por defecto (Invitado)
            return {
                "rol_asignado": "Observador",
                "peso_voto": 0.0,   # No pone nota
                "descripcion": "Invitado a la defensa."
            }