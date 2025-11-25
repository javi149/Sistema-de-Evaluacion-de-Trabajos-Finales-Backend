# 📋 Documentación de Rutas API

## Base URL
`http://localhost:5000` (o la URL de tu servidor)

---

## ✅ RUTAS DISPONIBLES

### 1. **ESTUDIANTES** (`/estudiantes`)
- `GET /estudiantes/` - Listar todos los estudiantes
- `GET /estudiantes/<id>` - Obtener estudiante por ID
- `POST /estudiantes/` - Crear estudiante
- `PUT /estudiantes/<id>` - Actualizar estudiante completo
- `PATCH /estudiantes/<id>` - Actualizar estudiante parcial
- `DELETE /estudiantes/<id>` - Eliminar estudiante
- `GET /estudiantes/<id>/trabajos` - Obtener trabajos de un estudiante ✅

---

### 2. **EVALUADORES** (`/evaluadores`)
- `GET /evaluadores/` - Listar todos los evaluadores
- `GET /evaluadores/<id>` - Obtener evaluador por ID
- `POST /evaluadores/` - Crear evaluador (requiere: nombre, tipo)
- `PUT /evaluadores/<id>` - Actualizar evaluador completo
- `DELETE /evaluadores/<id>` - Eliminar evaluador
- `GET /evaluadores/<id>/evaluaciones` - Obtener evaluaciones de un evaluador ✅

---

### 3. **TIPOS DE TRABAJO** (`/tipos-trabajo`)
- `GET /tipos-trabajo/` - Listar todos los tipos
- `GET /tipos-trabajo/<id>` - Obtener tipo por ID
- `POST /tipos-trabajo/` - Crear tipo
- `PUT /tipos-trabajo/<id>` - Actualizar tipo completo
- `PATCH /tipos-trabajo/<id>` - Actualizar tipo parcial
- `DELETE /tipos-trabajo/<id>` - Eliminar tipo

---

### 4. **TRABAJOS** (`/trabajos`)
- `GET /trabajos/` - Listar todos los trabajos
- `GET /trabajos/<id>` - Obtener trabajo por ID
- `POST /trabajos/` - Crear trabajo (requiere: titulo, tipo)
- `PUT /trabajos/<id>` - Actualizar trabajo completo
- `DELETE /trabajos/<id>` - Eliminar trabajo
- `GET /trabajos/estudiante/<estudiante_id>` - Obtener trabajos por estudiante ✅
- `GET /trabajos/<id>/evaluaciones` - Obtener evaluaciones de un trabajo ✅

---

### 5. **CRITERIOS** (`/criterios`)
- `GET /criterios/` - Listar todos los criterios
- `GET /criterios/<id>` - Obtener criterio por ID ✅
- `POST /criterios/` - Crear criterio
- `PUT /criterios/<id>` - Actualizar criterio ✅
- `PATCH /criterios/<id>` - Actualizar criterio parcial ✅
- `DELETE /criterios/<id>` - Eliminar criterio ✅

---

### 6. **EVALUACIONES** (`/evaluaciones`)
- `GET /evaluaciones/` - Listar todas las evaluaciones
- `GET /evaluaciones/<id>` - Obtener evaluación por ID ✅
- `POST /evaluaciones/` - Crear evaluación
- `GET /evaluaciones/trabajo/<trabajo_id>` - Obtener evaluaciones por trabajo ✅
- `GET /evaluaciones/evaluador/<evaluador_id>` - Obtener evaluaciones por evaluador ✅
- `PUT /evaluaciones/<id>` - Actualizar evaluación ✅
- `PATCH /evaluaciones/<id>` - Actualizar evaluación parcial ✅
- `DELETE /evaluaciones/<id>` - Eliminar evaluación ✅

---

### 7. **EVALUACIÓN DETALLE** (`/evaluacion-detalle`)
- `GET /evaluacion-detalle/` - Listar todos los detalles
- `GET /evaluacion-detalle/<id>` - Obtener detalle por ID
- `GET /evaluacion-detalle/evaluacion/<evaluacion_id>` - Listar detalles por evaluación
- `POST /evaluacion-detalle/` - Crear detalle
- `PUT /evaluacion-detalle/<id>` - Actualizar detalle completo
- `PATCH /evaluacion-detalle/<id>` - Actualizar detalle parcial
- `DELETE /evaluacion-detalle/<id>` - Eliminar detalle

---

### 8. **ACTAS** (`/actas`)
- `GET /actas/` - Listar todas las actas
- `GET /actas/<id>` - Obtener acta por ID
- `POST /actas/` - Crear acta
- `PUT /actas/<id>` - Actualizar acta completo
- `PATCH /actas/<id>` - Actualizar acta parcial
- `DELETE /actas/<id>` - Eliminar acta

---

### 9. **GENERACIÓN DE ACTAS** (`/generar-acta`)
- `GET /generar-acta/html/<trabajo_id>` - Generar acta en HTML
- `GET /generar-acta/texto/<trabajo_id>` - Generar acta en texto plano

---

### 10. **NOTAS** (`/api/calcular-nota`)
- `GET /api/calcular-nota/<trabajo_id>` - Calcular nota final ponderada ✅

---

## ✅ TODAS LAS RUTAS HAN SIDO IMPLEMENTADAS

Todas las rutas faltantes han sido agregadas y están disponibles para el frontend.

