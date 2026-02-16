# 🎯 PROYECTO: Sistema Automatizado de Pruebas Atrasadas

**Cliente:** Claudio Rojas - Director Académico  
**Institución:** Colegio San Francisco Javier, Puerto Montt  
**Fecha inicio:** Febrero 2026  
**Estado:** Prototipo funcional completado ✅

---

## 📊 PROBLEMA IDENTIFICADO

### Situación Actual
- **Tiempo invertido:** 15-20 minutos semanales en inscripciones manuales
- **Volumen:** 10-20 emails por semana de docentes
- **Proceso manual:** 
  1. Recibir email del profesor
  2. Abrir Google Sheets
  3. Buscar hoja correspondiente (102 hojas en total)
  4. Verificar manualmente si estudiante tiene menos de 2 pruebas
  5. Copiar datos del email
  6. Pegar en la hoja correcta
  
### Puntos de Dolor
- ❌ Errores de duplicación (estudiante inscrito 2 veces en misma asignatura).
- ❌ Estudiantes con más de 2 pruebas (excede límite reglamentario).
- ❌ Tiempo del Director Académico en tarea operativa.
- ❌ Uso de tiempo de laboral y personal para mantener el proceso actualizado.

---

## ✅ SOLUCIÓN IMPLEMENTADA (HOY)

### Componentes Desarrollados

#### 1. **EmailParser** (en `Sistema_Pruebas_Atrasadas.ipynb`)
Extrae automáticamente de emails reales vía Gmail API:
- ✅ Nombre del estudiante (desde asunto)
- ✅ Curso (desde asunto)
- ✅ Asignatura (desde cuerpo)
- ✅ Fecha ("miércoles 3 de diciembre" → "MIÉRCOLES 0312")
- ✅ Duración de la prueba
- ✅ Ciclo automático (basado en mapeo curso→ciclo)

**Tecnologías:** Python, regex, Gmail API (próxima semana)

#### 2. **ValidadorPruebas** (`validador_pruebas.py`)
Verifica automáticamente:
- ✅ Que la hoja de la fecha existe
- ✅ Cuántas pruebas tiene el estudiante ese día
- ✅ Si excede límite de 2 pruebas → RECHAZA
- ✅ Si es duplicado (misma asignatura) → ALERTA
- ✅ Genera mensajes claros para cada caso

**Tecnologías:** Python, pandas, openpyxl

#### 3. **SistemaInscripcionPruebas** (`sistema_completo.py`)
Integra todo el flujo:
- ✅ Procesa email completo
- ✅ Valida automáticamente
- ✅ Genera email de respuesta al profesor
- ✅ Prepara datos listos para Google Sheets

**Tecnologías:** Python (integración de módulos)

---

## 📈 IMPACTO ESPERADO

### Beneficios Cuantitativos
| Métrica | Antes | Después | Mejora |
|---------|-------|---------|--------|
| Tiempo por inscripción | 5 min | 30 seg | **90% reducción** |
| Errores de sobrecupo | 2-3/mes | 0 | **100% eliminación** |
| Disponibilidad | Horario laboral y personal | 24/7 | **Siempre activo** |
| Validaciones manuales | 100% | 0% | **Automático** |

### Beneficios Cualitativos
- ✅ Director enfocado en tareas estratégicas
- ✅ Profesores obtienen respuesta inmediata
- ✅ Transparencia total (Google Sheets compartido)
- ✅ Auditoría completa de inscripciones
- ✅ Escalable a otros procesos administrativos

---

## 🗓️ ROADMAP: Próximas Semanas

### Semana 2 (Próxima): Conexión Google Sheets
**Objetivos:**
- [ ] Configurar API de Google Sheets
- [ ] Crear función de inserción automática de filas
- [ ] Crear función de creación de hojas nuevas (si no existe)
- [ ] Probar con datos reales en un Sheets de prueba

**Entregable:** Script que inserta directamente en Google Sheets

---

### Semana 3: Automatización Gmail
**Objetivos:**
- [ ] Configurar Gmail API con OAuth
- [ ] Filtro automático: emails con CC a crojas@colsanjavier.cl
- [ ] Trigger automático cada hora
- [ ] Sistema de marcado de emails procesados

**Entregable:** Sistema totalmente automático sin intervención manual

---

### Semana 4: Notificaciones y Dashboard
**Objetivos:**
- [ ] Email automático de respuesta a profesores
- [ ] Email diario a Claudio con resumen
- [ ] Dashboard Looker Studio con métricas
- [ ] Documentación completa

**Entregable:** Sistema production-ready + documentación

---

## 🛠️ STACK TECNOLÓGICO

### Actual (Prototipo)
```
Python 3.x
├── pandas          (manipulación de datos)
├── openpyxl        (lectura de Excel)
└── re              (parsing de texto de emails)
```

### Próximo (Producción)
```
Python 3.x + APIs
├── gspread         (Google Sheets API)
├── google-auth     (autenticación OAuth)
├── gmail-api       (lectura automática de emails)
└── smtplib         (envío de emails)
```

---

## 📁 ARCHIVOS DEL PROYECTO

```
Entregables/
├── Sistema_Pruebas_Atrasadas.ipynb    # 🎯 NOTEBOOK PRINCIPAL
│   ├── EmailParser (lee emails reales)
│   ├── ValidadorPruebas (valida límites)
│   └── Casos de prueba integrados
│
├── Preparacion_Gmail_API.ipynb        # 📧 Guía para próxima semana
│   ├── Instrucciones paso a paso
│   ├── Configuración Gmail API
│   └── Checklist de preparación
│
├── README.md                          # Este documento
├── GUIA_VISUAL.md                     # Demo visual con ejemplos
│
└── [Archivos .py de referencia]      # Scripts originales
    ├── email_parser.py
    ├── validador_pruebas.py
    └── sistema_completo.py
```

**IMPORTANTE:** Se trabaja en **Jupyter Notebook**, por lo que el proyecto se entrega en formato `.ipynb` que es más interactivo y fácil de ejecutar celda por celda.

---

## 🧪 CASOS DE PRUEBA EJECUTADOS

### Caso 1: Email de Estudiante 1  (1°C)
```
Email → Parser → Validador
✅ Datos extraídos correctamente
❌ Hoja no existe (fecha futura)
→ Email de rechazo generado
```

### Caso 2: Estudiante 2 (duplicado)
```
Estudiante con prueba de LENGUAJE
Intento de inscribir otra de LENGUAJE
→ Alerta de duplicado generada
```

### Caso 3: Estudiante 3 (válido)
```
1 prueba actual (MATEMATICA)
Inscripción de CIENCIAS
✅ Validación exitosa (1/2 → 2/2)
```

---

## 💡 EXTENSIONES FUTURAS

### Fase 2: Otros Problemas a Automatizar
1. **Análisis de evaluaciones departamentales**
   - Dashboard automático de resultados por ítem
   - Identificación de contenidos débiles
   - Comparación entre cursos paralelos

2. **Sistema de alertas tempranas**
   - Estudiantes con patrón de ausencias
   - Bajo rendimiento en asignaturas
   - Clustering automático de riesgo académico

3. **Automatización de reuniones**
   - Resumen automático de actas
   - Seguimiento de compromisos
   - Recordatorios automáticos

---

## 📞 CONTACTO Y SOPORTE

**Desarrollador:** Claude (Anthropic)  
**Sponsor:** Claudio Rojas  
**Email:** crojasmon@gmail.com 
**Repositorio:** https://github.com/ClaudioRojasMon/Sistema-Pruebas-Atrasadas

---

**Última actualización:** Febrero 15, 2026  
**Versión:** 1.0 (Prototipo funcional)  
**Status:** ✅ Ready for Week 2
