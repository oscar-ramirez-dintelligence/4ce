# Aplicación de Gestión de Medios y Cotizaciones

Esta es una aplicación web full-stack construida con Flask, diseñada para la gestión integral de soportes publicitarios, agencias, cotizaciones y usuarios en una empresa de medios.

---

## 1. Arquitectura de la Aplicación

La aplicación sigue una arquitectura moderna y escalable, basada en las mejores prácticas de desarrollo con Flask.

-   **Framework Backend**: **Flask**. Se utiliza el patrón **Application Factory** (`create_app`) para inicializar la aplicación, lo que facilita la configuración y las pruebas.
-   **Estructura Modular**: La lógica está organizada en **Blueprints**, que son componentes modulares de Flask. Cada módulo principal (ej. `soportes`, `cotizaciones`, `admin`) tiene su propio blueprint, lo que mantiene el código limpio y organizado.
-   **Capa de Servicios**: Toda la lógica de negocio y las interacciones con la base de datos están encapsuladas en una **capa de servicios** (`servicios/*.py`). Las rutas de Flask solo se encargan de manejar las peticiones HTTP y llamar a estos servicios, siguiendo el principio de responsabilidad única.
-   **Base de Datos**: **Google Cloud Firestore** (en modo nativo) se utiliza como la base de datos NoSQL. Es una solución escalable y sin servidor, ideal para despliegues en la nube.
-   **Autenticación**: La gestión de usuarios (creación, inicio de sesión, contraseñas) se delega a **Firebase Authentication**. El backend de Flask se integra con el SDK de Admin de Firebase para gestionar los perfiles de usuario y verificar la identidad de los usuarios de forma segura.
-   **Gestión de Sesiones**: Para persistir el inicio de sesión del usuario de forma segura en entornos sin estado como Google Cloud Run, la aplicación utiliza **cookies firmadas por el servidor**. Después de que un usuario se autentica con Firebase en el frontend, se genera un token que el backend verifica para crear una sesión segura en una cookie. La integridad de esta cookie está garantizada por una `SECRET_KEY`.
-   **Frontend**: Las vistas se renderizan con plantillas **Jinja2** y el diseño responsivo se logra con **Bootstrap 5**. La interactividad, como la autenticación con Firebase y la visualización de mapas, se maneja con **JavaScript** en el lado del cliente.
-   **Geolocalización**: Se utiliza la **API de Google Maps JavaScript** para visualizar la ubicación de los soportes publicitarios en un mapa interactivo.

---

## 2. Configuración del Entorno

Sigue estos pasos para configurar y ejecutar el proyecto en un entorno de desarrollo local.

### Prerrequisitos
-   Python 3.10 o superior.
-   `pip` y `venv` instalados.
-   [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) instalado y configurado en tu máquina.

### Paso 1: Configurar la Autenticación de Google Cloud
La aplicación utiliza **Application Default Credentials (ADC)**. Para configurar esto en tu máquina local, ejecuta los siguientes comandos:
```bash
# Inicia sesión en tu cuenta de Google
gcloud auth login

# Configura las credenciales por defecto para las aplicaciones
gcloud auth application-default login
```

### Paso 2: Clonar y Preparar el Proyecto
```bash
# Clona el repositorio
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_DIRECTORIO>

# Crea y activa un entorno virtual
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar Dependencias
Instala todas las bibliotecas de Python necesarias:
```bash
pip install -r requirements.txt
```

### Paso 4: Configurar Variables de Entorno y Contraseñas
Crea un archivo `.env` en la raíz del proyecto. Puedes copiar el ejemplo y rellenarlo:
```bash
cp .env.example .env
```
Ahora, edita el archivo `.env` con tus propias claves y configuraciones:

```ini
# --- Configuración de Flask ---
# Usado por el comando 'flask run' para encontrar y ejecutar la app.
FLASK_APP=run.py
FLASK_ENV=development

# --- Clave Secreta de la Aplicación ---
# ESTA ES LA "CONTRASEÑA" PRINCIPAL DE LA APLICACIÓN.
# Se usa para firmar las cookies de sesión de forma segura.
# Debe ser una cadena larga, aleatoria y secreta.
# Puedes generar una con: python -c 'import secrets; print(secrets.token_hex(24))'
SECRET_KEY="tu_clave_super_secreta_y_larga_aqui"

# --- Configuración de Google Cloud ---
# El ID de tu proyecto en Google Cloud.
GOOGLE_CLOUD_PROJECT="tu-gcp-project-id"

# La clave de API de Google Maps para el frontend.
# Asegúrate de que la API "Maps JavaScript API" esté habilitada en tu proyecto.
GOOGLE_MAPS_API_KEY="tu_google_maps_api_key"

# --- Configuración de Firebase ---
# Opcional: Ruta al archivo JSON de la cuenta de servicio para el SDK de Admin.
# Déjalo en blanco si usas ADC (recomendado).
FIREBASE_ADMIN_SDK_CONFIG=""

# Configuración del SDK web de Firebase (para el frontend).
# Obtén esto desde: Firebase Console > Project Settings > General > Your apps > Web app > SDK setup and configuration > Config.
# IMPORTANTE: Usa comillas simples alrededor del JSON.
FIREBASE_WEB_CONFIG_JSON='{"apiKey": "AIza...", "authDomain": "...", "projectId": "...", "storageBucket": "...", "messagingSenderId": "...", "appId": "..."}'
```

### Paso 5: Poblar la Base de Datos
Para que la aplicación tenga datos con los que trabajar, ejecuta el script de seeding:
```bash
python seed_data.py
```

### Paso 6: Ejecutar la Aplicación
```bash
# Inicia el servidor de desarrollo de Flask
flask run
```
La aplicación estará disponible en `http://127.0.0.1:5000`.

---

## 3. Despliegue en Producción (Google Cloud Run)

Para desplegar en Cloud Run, el `Dockerfile` (no incluido aquí, pero sería el siguiente paso) usaría `gunicorn` para ejecutar la aplicación:
```bash
gunicorn 'cotizador:create_app()' --bind 0.0.0.0:8080
```
La instancia de Cloud Run deberá tener una **cuenta de servicio** asociada con los permisos necesarios (ej. "Editor de Cloud Datastore") para que la autenticación ADC funcione correctamente.
