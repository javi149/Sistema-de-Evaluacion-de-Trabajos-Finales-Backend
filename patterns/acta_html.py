from .acta_base import ActaBase

class ActaHTML(ActaBase):
    # Esta clase sigue las reglas del molde ActaBase
    
    def __init__(self):
        self.html = ""

    def crear_encabezado(self, datos):
        # Aqui creamos el titulo del acta
        titulo = datos.get('titulo_trabajo', 'Sin Título')
        self.html += f"<h1>ACTA DE EVALUACIÓN: {titulo}</h1><hr>"

    def crear_cuerpo(self, datos, evaluaciones):
        # Aqui ponemos la lista de notas
        self.html += "<h3>Detalle de Notas:</h3><ul>"
        for evaluacion in evaluaciones:
            # Usamos los nombres de columnas que vimos en tu base de datos
            nota = evaluacion.get('nota_final', 0)
            comentario = evaluacion.get('comentarios', 'Sin comentarios')
            self.html += f"<li>Nota: {nota} - Comentario: {comentario}</li>"
        self.html += "</ul>"

    def crear_firmas(self, evaluaciones):
        # Un espacio para las firmas al final
        self.html += "<br><p>__________________________<br>Firma Comisión</p>"

    def obtener_resultado(self):
        return self.html