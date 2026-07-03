# TalNext

Plataforma de entrevistas técnicas asistida por IA. Self-hosted y multi-usuario para equipos de reclutamiento.

Analiza CVs automáticamente, mide el fit con el rol, genera preguntas personalizadas según skills detectadas, evalúa las respuestas y produce reportes ejecutivos completos.

---

## Índice

- [Características](#características)
- [Requisitos](#requisitos)
- [Advertencias importantes](#advertencias-importantes)
- [Instalación](#instalación)
  - [1. Base de datos PostgreSQL](#1-base-de-datos-postgresql)
  - [2. Backend](#2-backend)
  - [3. Frontend](#3-frontend)
- [Primer uso](#primer-uso)
- [Roles y permisos](#roles-y-permisos)
- [Configuración](#configuración)
- [Mantenimiento](#mantenimiento)
- [Solución de problemas](#solución-de-problemas)

---

## Características

- Extracción automática de skills desde CVs (PDF, JPG, PNG)
- Análisis de fit CV vs. rol con puntaje objetivo
- Generación de preguntas técnicas y conductuales adaptadas al perfil
- Grabación y transcripción de respuestas por voz
- Reportes ejecutivos automatizados
- Comparación de múltiples candidatos por ronda
- Sistema multi-usuario con roles (Admin / Recruiter / Viewer)
- API keys de Groq cifradas por usuario
- Historial compartido en toda la empresa
- Interfaz bilingüe (español / inglés)
- Drag & drop para subida de archivos

---

## Requisitos

### Software

- **Python** 3.11 o superior
- **PostgreSQL** 14 o superior
- **Servidor web** para servir el frontend estático (nginx, Apache, IIS, Caddy, etc.)

### Cuentas de servicios

- **Groq API** — cada usuario que haga entrevistas necesita su propia API key ([console.groq.com/keys](https://console.groq.com/keys))

---

## ⚠️ Advertencias importantes

### Sobre las API keys de Groq

**Cada usuario debe agregar SU PROPIA API key de Groq** en la sección Configuración de la app. La key se guarda cifrada en el servidor y solo su propietario puede usarla.

### Tier de Groq recomendado: **Developer (pago)**

El tier gratuito de Groq tiene límites de **8000 tokens por minuto**, que son insuficientes para uso profesional. TalNext usa modelos GPT-OSS 120B con `reasoning_effort=high` para máxima calidad, y una sola entrevista puede consumir 15-25K tokens.

**Se recomienda encarecidamente el tier Developer de Groq:**

- Costo: **~$0.006 por entrevista** (menos de 1 centavo)
- 500 entrevistas/mes: **~$3.50**
- 1000 entrevistas/mes: **~$7**
- Se activa agregando una tarjeta en [console.groq.com/settings/billing](https://console.groq.com/settings/billing)
- Aumenta los límites 10x automáticamente
- La misma API key sigue funcionando

**Sin el tier Developer, la plataforma funcionará pero con errores frecuentes de rate limit** al procesar CVs grandes o generar entrevistas completas.

### Sobre las claves de cifrado

TalNext usa dos claves críticas en el archivo `.env`:

- `ENCRYPTION_KEY` — cifra las API keys de los usuarios
- `JWT_SECRET_KEY` — firma los tokens de autenticación

**Estas claves deben ser generadas al instalar y guardadas en un lugar seguro.** Si se pierden:
- `ENCRYPTION_KEY` perdida = las API keys guardadas no pueden descifrarse (los usuarios deben re-ingresarlas)
- `JWT_SECRET_KEY` perdida = todas las sesiones activas se invalidan (los usuarios deben re-loguearse)

---

## Instalación

### 1. Base de datos PostgreSQL

Conéctate a PostgreSQL como superusuario y crea la base de datos:

```sql
CREATE DATABASE talnext;
CREATE USER talnext_user WITH PASSWORD 'ELIGE_UNA_CONTRASEÑA_SEGURA';
GRANT ALL PRIVILEGES ON DATABASE talnext TO talnext_user;
```

**En PostgreSQL 15+, también otorga permisos sobre el schema public:**

```sql
\c talnext
GRANT ALL ON SCHEMA public TO talnext_user;
```

---

### 2. Backend

#### 2.1 Preparar el entorno

Entra a la carpeta `backend/`:

```bash
cd backend
```

Crea y activa un entorno virtual:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

Instala las dependencias:

```bash
pip install -r requirements.txt
```

#### 2.2 Configurar variables de entorno

Copia el archivo de ejemplo:

```bash
cp .env.example .env
```

Edita `.env` con los valores reales:

```env
APP_NAME=TalNext
DEBUG=False

# Modelos de Groq (no cambiar salvo indicación)
GROQ_MODEL=openai/gpt-oss-120b
GROQ_MODEL_FAST=openai/gpt-oss-20b

# Base de datos (ajustar según tu instalación)
DATABASE_URL=postgresql://talnext_user:TU_CONTRASEÑA@localhost:5432/talnext

# JWT (generar con el comando de abajo)
JWT_SECRET_KEY=GENERAR_CON_COMANDO
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=10080

# Cifrado de API keys (generar con el comando de abajo)
ENCRYPTION_KEY=GENERAR_CON_COMANDO

# Dominios permitidos para el frontend (separar con coma)
ALLOWED_ORIGINS=http://localhost:3000
```

**Generar `JWT_SECRET_KEY`:**

```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

Copia el resultado y pégalo en `JWT_SECRET_KEY`.

**Generar `ENCRYPTION_KEY`:**

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Copia el resultado y pégalo en `ENCRYPTION_KEY`.

> ⚠️ Guarda ambas claves en un gestor de contraseñas o lugar seguro antes de continuar.

#### 2.3 Configurar CORS

En `ALLOWED_ORIGINS`, pon la URL completa donde correrá el frontend:

**Ejemplos:**

```env
# Desarrollo local
ALLOWED_ORIGINS=http://localhost:3000

# Red interna sin dominio
ALLOWED_ORIGINS=http://192.168.1.50

# Con dominio y HTTPS
ALLOWED_ORIGINS=https://talnext.tu-empresa.com

# Varios dominios (separados por coma)
ALLOWED_ORIGINS=https://talnext.tu-empresa.com,https://app.tu-empresa.com
```

#### 2.4 Crear las tablas

Dentro de `backend/`:

```bash
python init_db.py
```

Esto crea todas las tablas necesarias.

#### 2.5 Arrancar el backend

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

El backend queda disponible en `http://TU_SERVIDOR:8000`.

Para desarrollo con auto-reload:

```bash
uvicorn main:app --reload
```

Para producción, ver la sección [Correr como servicio](#correr-como-servicio).

---

### 3. Frontend

El frontend ya viene compilado en la carpeta `frontend/`. No necesitas Flutter instalado.

#### 3.1 Configurar la URL del backend

Abre `frontend/config.json` y ajusta:

```json
{
  "apiUrl": "http://TU_SERVIDOR_BACKEND:8000"
}
```

**Ejemplos:**

```json
{ "apiUrl": "http://localhost:8000" }
```

```json
{ "apiUrl": "http://192.168.1.50:8000" }
```

```json
{ "apiUrl": "https://api.tu-empresa.com" }
```

#### 3.2 Servir el frontend

Copia todo el contenido de `frontend/` a tu servidor web.

**Con Nginx (Linux):**

```nginx
server {
    listen 80;
    server_name talnext.tu-empresa.com;
    root /var/www/talnext;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

**Con Python (para probar rápido):**

```bash
cd frontend
python -m http.server 3000
```

Abre `http://localhost:3000` en el navegador.

**Con IIS (Windows):**

Copia el contenido a `C:\inetpub\wwwroot\talnext\` y configura el sitio.

---

## Primer uso

### Crear el usuario administrador

La primera vez que abras el frontend, ve a `/register` y crea el usuario administrador principal. **El primer usuario registrado se vuelve automáticamente admin** y desactiva el auto-registro público.

### Configurar tu API key de Groq

1. Login como admin
2. Ve a **Configuración**
3. Pega tu API key de Groq (empieza con `gsk_...`)
4. Guarda

### Crear más usuarios

1. Ve a **Administración** (solo visible para admins)
2. Click en **Nuevo usuario**
3. Ingresa email, contraseña, nombre y rol
4. Cada usuario debe agregar su propia API key en Configuración después de loguearse

### Hacer tu primera entrevista

1. Home → **Nueva entrevista**
2. Sube el CV del candidato
3. Verifica las skills detectadas
4. Configura el rol y descripción
5. Ejecuta el análisis de fit
6. Genera las preguntas
7. Realiza la entrevista puntuando cada respuesta
8. Genera el reporte final

---

## Roles y permisos

| Acción | Admin | Recruiter | Viewer |
|--------|:-----:|:---------:|:------:|
| Ver historial de entrevistas | ✅ | ✅ | ✅ |
| Ver comparaciones | ✅ | ✅ | ✅ |
| Ver detalles de entrevistas | ✅ | ✅ | ✅ |
| Crear nuevas entrevistas | ✅ | ✅ | ❌ |
| Crear comparaciones | ✅ | ✅ | ❌ |
| Importar archivos `.cvtn` | ✅ | ✅ | ❌ |
| Eliminar entrevistas propias | ✅ | ✅ | ❌ |
| Eliminar entrevistas ajenas | ✅ | ❌ | ❌ |
| Gestionar usuarios | ✅ | ❌ | ❌ |
| Cambiar propio rol | ❌ | ❌ | ❌ |

**Nota:** Los admins pueden editar su propio nombre, email y contraseña, pero no su rol ni estado activo (otro admin debe hacerlo).

---

## Configuración

### Variables del `.env`

| Variable | Descripción | Requerida |
|----------|-------------|-----------|
| `APP_NAME` | Nombre visible de la app | No |
| `DEBUG` | Modo debug (`True`/`False`) | No |
| `GROQ_MODEL` | Modelo principal de Groq | Sí |
| `GROQ_MODEL_FAST` | Modelo rápido de Groq | Sí |
| `DATABASE_URL` | Conexión a PostgreSQL | **Sí** |
| `JWT_SECRET_KEY` | Firma tokens JWT | **Sí** |
| `JWT_ALGORITHM` | Algoritmo JWT (usar `HS256`) | Sí |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | Duración del token (default: 7 días) | Sí |
| `ENCRYPTION_KEY` | Cifra API keys de usuarios | **Sí** |
| `ALLOWED_ORIGINS` | Dominios que pueden acceder al backend | **Sí** |

### Rate limits

Los siguientes endpoints tienen rate limit por IP:

- `POST /api/v1/auth/login` — 5 intentos por minuto
- `POST /api/v1/auth/login-form` — 5 intentos por minuto
- `POST /api/v1/auth/register` — 3 intentos por hora

---

## Mantenimiento

### Correr como servicio

**Linux (systemd):**

Crea `/etc/systemd/system/talnext.service`:

```ini
[Unit]
Description=TalNext Backend
After=network.target postgresql.service

[Service]
User=talnext
WorkingDirectory=/opt/talnext/backend
Environment="PATH=/opt/talnext/backend/venv/bin"
ExecStart=/opt/talnext/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Activa el servicio:

```bash
sudo systemctl daemon-reload
sudo systemctl enable talnext
sudo systemctl start talnext
sudo systemctl status talnext
```

**Windows:**

Usa NSSM (Non-Sucking Service Manager) o Task Scheduler para correr uvicorn como servicio.

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
