# 🔌 Endpoints del Backend

**Base URL:** `http://localhost:5000` (Local) o `https://sistema-de-evaluacion-de-trabajos-finales-production.up.railway.app` (Producción/Railway)

Aquí tienes el listado completo de rutas disponibles para conectar tu frontend.

## 1. Estudiantes (`/estudiantes`)
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `GET` | `/estudiantes/` | Listar todos los estudiantes |
| `POST` | `/estudiantes/` | Crear un nuevo estudiante |
| `GET` | `/estudiantes/<id>` | Obtener detalle de un estudiante |
| `PUT` | `/estudiantes/<id>` | Actualizar estudiante (completo) |
| `PATCH` | `/estudiantes/<id>` | Actualizar estudiante (parcial) |
| `DELETE` | `/estudiantes/<id>` | Eliminar estudiante |

## 2. Evaluadores (`/evaluadores`)
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `GET` | `/evaluadores/` | Listar todos los evaluadores |
| `POST` | `/evaluadores/` | Crear evaluador (Usa Factory para rol/tipo) |
| `GET` | `/evaluadores/<id>` | Obtener detalle de un evaluador |
| `PUT` | `/evaluadores/<id>` | Actualizar evaluador |
| `DELETE` | `/evaluadores/<id>` | Eliminar evaluador |
| `GET` | `/evaluadores/<id>/evaluaciones` | Ver evaluaciones hechas por este evaluador |

## 3. Trabajos (`/trabajos`)
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `GET` | `/trabajos/` | Listar todos los trabajos |
| `POST` | `/trabajos/` | Crear trabajo (Usa Factory para reglas) |
| `GET` | `/trabajos/<id>` | Obtener detalle de un trabajo |
| `PUT` | `/trabajos/<id>` | Actualizar trabajo |
| `DELETE` | `/trabajos/<id>` | Eliminar trabajo |
| `GET` | `/trabajos/estudiante/<id>` | Listar trabajos de un estudiante específico |
| `GET` | `/trabajos/<id>/evaluaciones` | Ver evaluaciones recibidas por este trabajo |

## 4. Evaluaciones (`/evaluaciones`)
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `GET` | `/evaluaciones/` | Listar todas las evaluaciones |
| `POST` | `/evaluaciones/` | Crear una evaluación (cabecera) |
| `GET` | `/evaluaciones/<id>` | Obtener una evaluación por ID |
| `PUT` | `/evaluaciones/<id>` | Actualizar evaluación (completo) |
| `PATCH` | `/evaluaciones/<id>` | Actualizar evaluación (parcial) |
| `DELETE` | `/evaluaciones/<id>` | Eliminar evaluación |
| `GET` | `/evaluaciones/trabajo/<id>` | Listar evaluaciones de un trabajo |
| `GET` | `/evaluaciones/evaluador/<id>` | Listar evaluaciones de un evaluador |

## 5. Detalle de Evaluación (`/evaluacion-detalle`)
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `GET` | `/evaluacion-detalle/` | Listar todos los detalles (notas por criterio) |
| `POST` | `/evaluacion-detalle/` | Agregar una nota por criterio |
| `GET` | `/evaluacion-detalle/<id>` | Obtener un detalle específico |
| `PUT` | `/evaluacion-detalle/<id>` | Actualizar detalle (completo) |
| `PATCH` | `/evaluacion-detalle/<id>` | Actualizar detalle (parcial) |
| `DELETE` | `/evaluacion-detalle/<id>` | Eliminar detalle |
| `GET` | `/evaluacion-detalle/evaluacion/<id>` | Listar detalles de una evaluación específica |

## 6. Criterios (`/criterios`)
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `GET` | `/criterios/` | Listar criterios de evaluación |
| `POST` | `/criterios/` | Crear nuevo criterio |
| `GET` | `/criterios/<id>` | Obtener criterio |
| `PUT` | `/criterios/<id>` | Actualizar criterio (completo) |
| `PATCH` | `/criterios/<id>` | Actualizar criterio (parcial) |
| `DELETE` | `/criterios/<id>` | Eliminar criterio |

## 7. Tipos de Trabajo (`/tipos-trabajo`)
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `GET` | `/tipos-trabajo/` | Listar tipos de trabajo |
| `POST` | `/tipos-trabajo/` | Crear tipo de trabajo |
| `GET` | `/tipos-trabajo/<id>` | Obtener tipo de trabajo |
| `PUT` | `/tipos-trabajo/<id>` | Actualizar tipo de trabajo (completo) |
| `PATCH` | `/tipos-trabajo/<id>` | Actualizar tipo de trabajo (parcial) |
| `DELETE` | `/tipos-trabajo/<id>` | Eliminar tipo de trabajo |

## 8. Actas (`/actas`)
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `GET` | `/actas/` | Listar actas generadas |
| `POST` | `/actas/` | Registrar una nueva acta (manual) |
| `PUT` | `/actas/<id>` | Actualizar acta |
| `PATCH` | `/actas/<id>` | Actualizar acta (parcial) |
| `DELETE` | `/actas/<id>` | Eliminar acta |
| `GET` | `/actas/generar/html/<trabajo_id>` | **Generar Acta en HTML** (Visualización) |
| `GET` | `/actas/generar/texto/<trabajo_id>` | **Generar Acta en Texto** (Descarga simple) |

## 9. Cálculo de Notas (`/api`)
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `GET` | `/api/calcular-nota/<trabajo_id>` | Calcular nota final ponderada de un trabajo |
