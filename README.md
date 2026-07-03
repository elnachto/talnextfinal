### Restaurar backup

```bash
psql -U talnext_user talnext < talnext_backup.sql
```

### Actualizar la app

1. Detén el backend
2. Backup de la base de datos
3. Reemplaza los archivos de `backend/` (excepto `.env` y `venv/`)
4. Reinstala dependencias: `pip install -r requirements.txt`
5. Ejecuta migraciones si aplica
6. Reemplaza el contenido de `frontend/` (mantén tu `config.json`)
7. Reinicia el backend

---

## Solución de problemas

### El frontend muestra "Error de conexión"

**Verifica:**

1. El backend está corriendo (`http://TU_SERVIDOR:8000/docs` debería mostrar la documentación)
2. `frontend/config.json` apunta a la URL correcta del backend
3. `ALLOWED_ORIGINS` en `.env` incluye la URL del frontend
4. No hay firewall bloqueando el puerto del backend

### Error 429 "Too Many Requests"

Los rate limits de login se activaron. Espera 1 minuto y vuelve a intentar.

### Error "No Groq API key configured"

El usuario debe ir a **Configuración** y agregar su propia API key de Groq.

### Error "Rate limit reached" al procesar CVs

Estás en el tier gratuito de Groq y llegaste al límite de tokens/minuto. **Se recomienda upgradear al tier Developer** ([console.groq.com/settings/billing](https://console.groq.com/settings/billing)) para eliminar este problema. Ver [Advertencias](#-advertencias-importantes).

### Error al detectar skills / generar preguntas

Verifica que tu API key de Groq sea válida en [console.groq.com/keys](https://console.groq.com/keys).

### El micrófono no funciona

- Chrome requiere HTTPS para grabar audio en producción (localhost está OK)
- El usuario debe dar permiso en el diálogo del navegador
- Verifica que no haya otra app usando el micrófono

### La app no carga después de compilar

- Verifica que `config.json` se haya copiado al servidor
- Abre la consola del navegador (F12) y revisa los errores
- Asegúrate de que el servidor web sirva `.json` correctamente

### Los usuarios no pueden ver entrevistas de otros

Esto es intencional si están usando la opción "Solo mías" en el filtro del historial. Desactívala para ver todas las entrevistas del equipo.

---

## Seguridad recomendada para producción

- Usa **HTTPS** en producción con certificado válido (Let's Encrypt es gratis)
- Genera claves fuertes para `JWT_SECRET_KEY` y `ENCRYPTION_KEY`
- Restringe `ALLOWED_ORIGINS` solo al dominio real del frontend
- Usa contraseñas fuertes para PostgreSQL
- Mantén Python, PostgreSQL y las dependencias actualizadas
- Configura backups automáticos de la base de datos
- Revisa los logs de acceso periódicamente

---

## Licencia

Software propietario. Uso interno bajo licencia comercial.

## Soporte

Para soporte técnico contacta a: `[tu-email@ejemplo.com]`

---

**TalNext v1.0**