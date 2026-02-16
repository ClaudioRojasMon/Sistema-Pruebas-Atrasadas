# Contribuyendo al Sistema de Pruebas Atrasadas

¡Gracias por tu interés en contribuir! Este documento proporciona pautas para contribuir al proyecto.

## 🤝 Código de Conducta

- Sé respetuoso y profesional
- Acepta críticas constructivas
- Enfócate en lo mejor para la comunidad
- Muestra empatía hacia otros miembros

## 🚀 Cómo Contribuir

### Reportar Bugs

1. Verifica que el bug no haya sido reportado antes
2. Crea un Issue con:
   - Descripción clara del problema
   - Pasos para reproducirlo
   - Comportamiento esperado vs actual
   - Logs relevantes
   - Versión de Python y sistema operativo

### Sugerir Mejoras

1. Verifica que la mejora no esté ya propuesta
2. Crea un Issue describiendo:
   - El problema que resuelve
   - Cómo beneficiaría al proyecto
   - Posible implementación

### Pull Requests

1. **Fork** el repositorio
2. **Crea una rama** desde `main`:
   ```bash
   git checkout -b feature/mi-nueva-caracteristica
   ```
3. **Realiza tus cambios** siguiendo el estilo del código
4. **Prueba** tus cambios completamente
5. **Commit** con mensajes descriptivos:
   ```bash
   git commit -m "feat: Agregar validación de emails duplicados"
   ```
6. **Push** a tu fork:
   ```bash
   git push origin feature/mi-nueva-caracteristica
   ```
7. **Abre un Pull Request** describiendo:
   - Qué cambia
   - Por qué es necesario
   - Cómo probaste los cambios

## 📝 Estándares de Código

### Python
- Usar PEP 8
- Docstrings para todas las funciones y clases
- Type hints cuando sea posible
- Nombres descriptivos de variables

### Commits
- Usar conventional commits: `feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`
- Mensajes en español
- Descripción clara y concisa

### Documentación
- Actualizar README.md si es necesario
- Comentar código complejo
- Incluir ejemplos de uso

## 🧪 Testing

- Probar con emails reales antes de enviar PR
- Verificar que no rompa funcionalidad existente
- Incluir casos de prueba para nuevas características

## 📋 Áreas de Contribución

### Prioridad Alta
- [ ] Mejoras en la detección de errores
- [ ] Optimización del parser de emails
- [ ] Mejor manejo de excepciones

### Prioridad Media
- [ ] Dashboard de estadísticas
- [ ] Exportación de reportes
- [ ] Notificaciones adicionales

### Prioridad Baja
- [ ] Interfaz web
- [ ] App móvil
- [ ] Integración con otros sistemas

## 💡 ¿Dudas?

Abre un Issue con la etiqueta `question` o contacta a:
- Email: crojas@colsanjavier.cl

---

¡Gracias por contribuir al proyecto! 🎉
