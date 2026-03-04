# Prospeo Enrich API

API para enriquecer datos de perfiles de LinkedIn usando la API de Prospeo.

## Requisitos

- Python 3.9+
- pip

## Instalación

1. Clonar el repositorio:
```bash
git clone <repo-url>
cd FastApi-local
```

2. Crear entorno virtual (opcional pero recomendado):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Crear archivo `.env`:
```bash
cp .env.example .env
```

5. Editar `.env` con tus credenciales de Prospeo:
```
# Prospeo API Configuration
PROSPEO_API_KEY=tu_api_key_aqui
PROSPEO_ENDPOINT=https://api.prospeo.io/enrich-person
PROSPEO_MAX_RETRIES=3
PROSPEO_DELAY_BETWEEN_REQUESTS=2
```

## Ejecución

```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8001
```

## Endpoints

### Enrich Simple
```bash
POST http://localhost:8001/enrich
```
Body:
```json
{
  "linkedin_url": "https://www.linkedin.com/in/usuario"
}
```

### Enrich Batch
```bash
POST http://localhost:8001/enrich/batch
```
Body:
```json
{
  "urls": [
    "https://www.linkedin.com/in/usuario1",
    "https://www.linkedin.com/in/usuario2"
  ]
}
```

### Bulk Enrich (desde Excel)
```bash
POST http://localhost:8001/bulk/enrich
```
Sin body. Lee el archivo `data/input.xlsx` y devuelve los datos enriquecidos en JSON.

## Estructura del Excel

El archivo `data/input.xlsx` debe tener una columna `profileUrl` con las URLs de LinkedIn.

## Licencia

MIT
