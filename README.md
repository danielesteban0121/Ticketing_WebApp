# Ticketing WebApp - Microservicios

Esta repo contiene tres microservicios FastAPI:

- `ms-categories`
- `ms-cities`
- `ms-points-of-sale`

Requisitos principales:

- Python 3.11+ (la imagen de Render usó 3.13 en el build)
- `requirements.txt` en la raíz contiene `fastapi`, `uvicorn`, `gunicorn`

Ejecutar localmente (PowerShell):

```powershell
# Crear y activar venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt

# Iniciar cada servicio en terminales separadas
uvicorn ms-categories.main:app --reload --port 8001
uvicorn ms-cities.main:app --reload --port 8002
uvicorn ms-points-of-sale.main:app --reload --port 8003
```

Despliegue en Render (monorepo)
- Ya hay un `render.yaml` en la raíz que define 3 Web Services. Cuando conectes el repo a Render, el `render.yaml` puede crear los servicios automáticamente.
- Nota: cada servicio ejecuta `pip install -r ../requirements.txt` en su `buildCommand` para usar el `requirements.txt` de la raíz.

Alternativa (crear servicios manualmente en la consola Render):
- Para cada servicio: `root directory` = `ms-categories` (o `ms-cities` / `ms-points-of-sale`).
- Build command: `pip install -r ../requirements.txt`
- Start command (actual en `render.yaml`):
  - `uvicorn ms-categories.main:app --host 0.0.0.0 --port $PORT --workers 2`
  - `uvicorn ms-cities.main:app --host 0.0.0.0 --port $PORT --workers 2`
  - `uvicorn ms-points-of-sale.main:app --host 0.0.0.0 --port $PORT --workers 2`

Por qué `uvicorn` vs `gunicorn`:
- `uvicorn` es el servidor ASGI; en producción puedes usar `gunicorn` como proceso maestro y `uvicorn.workers.UvicornWorker` como workers (recomendado para entornos con necesidades avanzadas de gestión de procesos). En muchos casos `uvicorn --workers N` funciona correctamente y es suficiente; por simplicidad aquí usamos `uvicorn` directamente.

Autenticación
- El token global para endpoints administrativos está en `auth/auth.py`:
  - `DANIELYKEVIN123`
- En las solicitudes, enviar header: `Authorization: Bearer DANIELYKEVIN123`

Ejemplos de llamadas (PowerShell):

```powershell
$body = @{ name="Teatro"; description="Obras y presentaciones" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8001/categories" -Method Post -Headers @{ Authorization = "Bearer DANIELYKEVIN123" } -Body $body -ContentType "application/json"
```

Cómo obtener las URLs públicas después del deploy
- En el Dashboard de Render, entra en cada Web Service y copia la URL (p. ej. `https://ms-categories.onrender.com`).

Si quieres, puedo:
- Crear un script `run-all.ps1` para abrir las 3 instancias localmente en terminales separadas, o
- Cambiar los `startCommand` en `render.yaml` para usar `gunicorn` en lugar de `uvicorn`.
