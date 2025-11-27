# 🚀 Guía Paso a Paso: Desplegar en Render

## Opción 1: Deploy Automático (Recomendado - usa render.yaml)

### Paso 1: Conecta tu repositorio a Render
1. Ve a https://dashboard.render.com
2. Haz click en **"New +"** → **"Blueprint"**
3. Selecciona **"Connect a repository"**
4. Busca y selecciona **`Ticketing_WebApp`**
5. Click en **"Connect"**

### Paso 2: Configura el Blueprint
1. En la pantalla de configuración, deja los valores por defecto
2. Render detectará automáticamente `render.yaml`
3. Click en **"Create Resources"**

**Render creará automáticamente:**
- ✅ ms-categories (servicio 1)
- ✅ ms-cities (servicio 2)
- ✅ ms-points-of-sale (servicio 3)

**Tiempo de despliegue:** ~2-3 minutos por servicio

### Paso 3: Espera a que termine
Irás a la pantalla de despliegue y verás los 3 servicios construyéndose. Los logs mostrarán:
```
🚀 [RENDER] Categories Microservice iniciando...
[INFO] Starting gunicorn 23.0.0
✅ [RENDER] Categories Microservice está listo.
Your service is live 🎉
```

---

## Opción 2: Deploy Manual (Si el Blueprint falla)

### Paso 1: Crea el primer servicio (ms-categories)

1. Ve a https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Selecciona tu repositorio `Ticketing_WebApp`
4. Configura:
   - **Name:** `ms-categories`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn -k uvicorn.workers.UvicornWorker ms-categories.main:app --bind 0.0.0.0:$PORT --workers 2`
5. Click **"Create Web Service"**

### Paso 2: Crea el segundo servicio (ms-cities)

1. Click **"New +"** → **"Web Service"** (nuevamente)
2. Mismo repositorio
3. Configura:
   - **Name:** `ms-cities`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn -k uvicorn.workers.UvicornWorker ms-cities.main:app --bind 0.0.0.0:$PORT --workers 2`
4. Click **"Create Web Service"**

### Paso 3: Crea el tercer servicio (ms-points-of-sale)

1. Click **"New +"** → **"Web Service"** (nuevamente)
2. Mismo repositorio
3. Configura:
   - **Name:** `ms-points-of-sale`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn -k uvicorn.workers.UvicornWorker ms-points-of-sale.main:app --bind 0.0.0.0:$PORT --workers 2`
4. Click **"Create Web Service"**

---

## Paso 4: Verifica que los servicios estén Live

1. Espera ~5 minutos para que terminen los builds
2. En Dashboard, verás los 3 servicios con estado **"Live"** (verde)
3. Cada uno tendrá una URL pública como:
   - `https://ms-categories-xxxx.onrender.com`
   - `https://ms-cities-xxxx.onrender.com`
   - `https://ms-points-of-sale-xxxx.onrender.com`

---

## Paso 5: Configura Variables de Entorno (Opcional)

Si quieres cambiar el token de autenticación en Render:

1. En cada servicio, ve a **Settings**
2. Scroll a **"Environment"**
3. Agrega:
   ```
   AUTH_TOKEN=Tu_Token_Aqui
   ```
4. Click **"Save Changes"**
5. Render reiniciará automáticamente los servicios

---

## Paso 6: Prueba los Endpoints

### Health Check (sin autenticación)
```bash
curl https://ms-categories-xxxx.onrender.com/health
```
Respuesta esperada:
```json
{
  "status": "ok",
  "service": "categories"
}
```

### Crear Categoría (requiere token)
```bash
curl -X POST https://ms-categories-xxxx.onrender.com/categories \
  -H "Authorization: Bearer DANIELYKEVIN123" \
  -H "Content-Type: application/json" \
  -d '{"name":"Conciertos","description":"Eventos de música"}'
```

### Obtener todas las categorías (sin autenticación)
```bash
curl https://ms-categories-xxxx.onrender.com/categories
```

---

## Logs de Render

Para ver los logs en tiempo real:
1. Entra a cada servicio en Dashboard
2. Click en **"Logs"**
3. Verás:
   ```
   🚀 [RENDER] Categories Microservice iniciando...
   ✅ [RENDER] Categories Microservice está listo.
   ```

---

## Solución de Problemas

### ❌ Error: "Could not open requirements file"
**Causa:** Render intenta instalar en el directorio incorrecto
**Solución:** En `render.yaml`, asegúrate de que:
```yaml
buildCommand: pip install -r ../requirements.txt
```
(nota el `../`)

### ❌ Error: "ModuleNotFoundError: No module named 'auth'"
**Causa:** Python path incorrecto
**Solución:** Verificar que `auth/__init__.py` existe y que `sys.path` está configurado en los `main.py`

### ❌ El servicio se reinicia constantemente
**Causa:** Error en el inicio o worker crash
**Solución:** Revisa los logs. Busca `[RENDER]` para identificar el error exacto.

### ❌ Conexión rechazada (Connection refused)
**Causa:** El servicio aún se está construyendo o inició pero no está listo
**Solución:** Espera 2-3 minutos y vuelve a intentar. Verifica que en logs dice "Your service is live"

---

## URLs de los Servicios (Ejemplos)

Después del deploy, tendrás URLs como:

| Servicio | URL Ejemplo |
|----------|-----------|
| Categories | https://ticketing-webapp.onrender.com |
| Cities | https://ticketing-webapp-1.onrender.com |
| Points of Sale | https://ticketing-webapp-2.onrender.com |

**Guarda estas URLs** - las necesitarás para las pruebas y documentación final.

---

## Próximos Pasos Después del Deploy

1. ✅ Guarda las 3 URLs públicas
2. ✅ Prueba cada endpoint con `curl` o Postman
3. ✅ Verifica los logs en Dashboard
4. ✅ Entrega las URLs a tu cliente/profesor

¡Listo para producción! 🎉
