from .acta_base import ActaBase

class ActaTexto(ActaBase):
    """
    Implementación concreta para generar actas en Texto Plano (.txt)
    """
    def __init__(self):
        self.texto = ""

    def _iniciar_documento(self):
        self.texto = "==================================================\n"

    def _generar_encabezado(self, datos):
        self.texto += "              ACTA DE EVALUACIÓN FINAL\n"
        self.texto += "==================================================\n\n"
        self.texto += f"FECHA: {datos.get('fecha_actual', '---')}\n"
        # Asumimos que viene el nombre de la institución
        self.texto += f"INSTITUCIÓN: {datos.get('institucion', 'Instituto Profesional')}\n\n"

    def _generar_info_estudiante(self, datos):
        self.texto += "--- ANTECEDENTES DEL ESTUDIANTE ---\n"
        self.texto += f"ESTUDIANTE: {datos.get('estudiante_nombre')} {datos.get('estudiante_apellido')}\n"
        self.texto += f"RUT: {datos.get('estudiante_rut', 'Sin RUT')}\n"
        self.texto += f"TRABAJO: {datos.get('titulo_trabajo')}\n"
        self.texto += "-----------------------------------\n\n"

    def _generar_detalle_evaluadores(self, evaluaciones):
        self.texto += "--- DETALLE DE LA COMISIÓN ---\n"
        for ev in evaluaciones:
            self.texto += f"[Evaluador ID {ev['evaluador_id']}]\n"
            self.texto += f"   > Nota: {ev['nota_final']}\n"
            self.texto += f"   > Obs:  {ev['comentarios']}\n"
        self.texto += "\n"

    def _generar_conclusion_nota(self, evaluaciones):
        if evaluaciones:
            promedio = sum(e['nota_final'] for e in evaluaciones) / len(evaluaciones)
            estado = "APROBADO" if promedio >= 4.0 else "REPROBADO"
        else:
            promedio = 0.0
            estado = "PENDIENTE"
            
        self.texto += "==================================================\n"
        self.texto += f"NOTA FINAL: {promedio:.2f}\n"
        self.texto += f"ESTADO:     {estado}\n"
        self.texto += "==================================================\n\n"

    def _generar_firmas(self, evaluaciones):
        self.texto += "\n\n"
        self.texto += "___________________          ___________________\n"
        self.texto += "  Firma Comisión               Firma Ministro de Fe\n"

    def _cerrar_documento(self):
        self.texto += "\nFIN DEL DOCUMENTO."

    def _obtener_resultado(self):
        return self.texto