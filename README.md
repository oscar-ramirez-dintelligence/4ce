# Aplicación de Gestión de Medios y Cotizaciones

Esta es una aplicación web full-stack construida con Flask, diseñada para la gestión integral de soportes publicitarios, agencias, cotizaciones y usuarios en una empresa de medios.

---

## 1. Arquitectura de la Aplicación

La aplicación sigue una arquitectura moderna y escalable, basada en las mejores prácticas de desarrollo con Flask.

-   **Framework Backend**: **Flask** con patrón **Application Factory** y **Blueprints** para una estructura modular.
-   **Capa de Servicios**: La lógica de negocio está encapsulada en una **capa de servicios** (`servicios/*.py`).
-   **Base de Datos**: **Google Cloud Firestore** se utiliza como la base de datos NoSQL.
-   **Autenticación**: Se implementa un **sistema de autenticación personalizado**. Las contraseñas de los usuarios se hashean de forma segura utilizando `werkzeug.security` (`sha256`) y se almacenan en la colección `usuarios` de Firestore.
-   **Gestión de Sesiones**: La aplicación utiliza **cookies firmadas por el servidor** para mantener la sesión del usuario. La `SECRET_KEY` para firmar estas cookies se gestiona como una variable de entorno.
-   **Frontend**: Vistas renderizadas con **Jinja2**, diseño responsivo con **Bootstrap 5**, y **JavaScript** para interactividad.
-   **Geolocalización**: **API de Google Maps JavaScript** para la visualización de soportes.

---

## 2. Configuración del Entorno

### Prerrequisitos
-   Python 3.10 o superior.
-   `pip` y `venv`.
-   [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) instalado y configurado.

### Paso 1: Autenticación de Google Cloud
Configura las credenciales por defecto para el desarrollo local:
```bash
gcloud auth application-default login
```

### Paso 2: Preparar el Proyecto
```bash
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_DIRECTORIO>
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Paso 3: Configurar Variables de Entorno
Crea un archivo `.env` a partir del ejemplo (`cp .env.example .env`) y edítalo:

```ini
# --- Configuración de Flask ---
FLASK_APP=run.py
FLASK_ENV=development

# --- Clave Secreta de la Aplicación ---
# Usada para firmar las cookies de sesión. Debe ser una cadena larga y aleatoria.
SECRET_KEY="tu_clave_super_secreta_y_larga_aqui"

# --- Configuración de Google Cloud ---
# El ID de tu proyecto en Google Cloud.
GOOGLE_CLOUD_PROJECT="tu-gcp-project-id"
# La clave de API de Google Maps para el frontend.
GOOGLE_MAPS_API_KEY="tu_google_maps_api_key"
```

### Paso 4: Poblar la Base de Datos
Para crear datos de prueba iniciales, ejecuta:
```bash
python seed_data.py
```

### Paso 5: Ejecutar la Aplicación
```bash
flask run
```
La aplicación estará disponible en `http://127.0.0.1:5000`.

---

## 3. Despliegue en Producción (Google Cloud Run)

El comando para producción es:
```bash
gunicorn 'cotizador:create_app()' --bind 0.0.0.0:8080
```
Asegúrate de que la cuenta de servicio de la instancia de Cloud Run tenga los permisos necesarios para Firestore (ej. rol "Editor de Cloud Datastore").
