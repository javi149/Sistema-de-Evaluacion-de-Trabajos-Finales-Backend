# models/__init__.py

# Importamos todos los modelos para que Flask y SQLAlchemy los reconozcan.
# El orden no es estricto, pero ayuda a mantener el orden lógico.

from .actas import Acta
from .criterios import Criterio
from .estudiantes import Estudiante
from evaluacion_detalle import EvaluacionDetalle
from .evaluaciones import Evaluacion
from .evaluadores import Evaluador
from .instituciones import Institucion
from .tipos_trabajo import TipoTrabajo
from .trabajos import Trabajo

# Si en el futuro agregas más tablas, recuerda importarlas aquí.
