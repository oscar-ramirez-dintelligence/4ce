# Cotizador de Medios Publicitarios (Refactorizado)

Una aplicación web construida con Flask y Google Cloud Firestore para gestionar soportes publicitarios, clientes y cotizaciones. Esta versión ha sido **refactorizada** para seguir las mejores prácticas de Flask, utilizando el patrón **Application Factory** y **Blueprints** para una estructura modular, escalable y mantenible.

## Autenticación con Google Cloud

Esta aplicación utiliza **Application Default Credentials (ADC)** para autenticarse con los servicios de Google Cloud (Firestore). Esto significa que **no es necesario** gestionar archivos de clave de cuenta de servicio (`.json`) manualmente. La autenticación se maneja automáticamente según el entorno.

---

## Guía de Instalación y Ejecución

### 1. Prerrequisitos

-   Python 3.13 o superior.
-   `pip` y `venv`.
-   [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) instalado y configurado en tu máquina local.
-   Una cuenta de Google Cloud con un proyecto activo.

### 2. Configuración del Proyecto en Google Cloud

1.  **Habilitar APIs**: En la consola de Google Cloud, asegúrate de que las siguientes APIs están habilitadas para tu proyecto:
    -   **Cloud Firestore API**
    -   **Maps JavaScript API**

2.  **Crear una Clave de API de Google Maps**:
    -   Ve a "APIs y Servicios" > "Credenciales".
    -   Haz clic en "Crear credenciales" > "Clave de API".
    -   Copia esta clave. La necesitarás para el archivo `.env`.

### 3. Configuración del Entorno Local

1.  **Autenticación Local con `gcloud`**:
    -   Asegúrate de haber iniciado sesión en gcloud: `gcloud auth login`.
    -   Configura las credenciales por defecto de la aplicación:
        ```bash
        gcloud auth application-default login
        ```

2.  **Clonar el Repositorio** y navegar al directorio.

3.  **Crear y Activar un Entorno Virtual**:
    ```bash
    python3 -m venv venv && source venv/bin/activate
    ```

4.  **Instalar Dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Configurar Variables de Entorno**:
    -   Crea una copia de `.env.example` y renómbrala a `.env`.
    -   Rellena las variables con tus propias claves y configuraciones:
        ```ini
        # --- Flask Configuration ---
        FLASK_APP=run.py
        FLASK_ENV=development

        # --- Application Configuration ---
        # Genera una clave segura con: python -c 'import secrets; print(secrets.token_hex(24))'
        SECRET_KEY="tu_clave_secreta_aqui"

        # --- Google Cloud Configuration ---
        GOOGLE_CLOUD_PROJECT="tu-gcp-project-id-aqui"
        GOOGLE_MAPS_API_KEY="tu_google_maps_api_key_aqui"
        ```

### 4. Poblar la Base de Datos (Seeding)

Ejecuta el script de seeding para poblar Firestore con datos de prueba:
```bash
python seed_data.py
```

### 5. Ejecutar la Aplicación

**A. Modo de Desarrollo:**
Gracias a las variables `FLASK_APP` y `FLASK_ENV` en el archivo `.env`, puedes iniciar la aplicación simplemente con:
```bash
flask run
```
La aplicación estará disponible en `http://127.0.0.1:5000`.

**B. Modo de Producción (para Cloud Run):**
-   Asegúrate de que la cuenta de servicio de tu instancia de Cloud Run tenga el rol de **Editor de Cloud Datastore**.
-   Despliega la aplicación. Gunicorn se iniciará con el siguiente comando:
    ```bash
    gunicorn 'cotizador:create_app()' --bind 0.0.0.0:8080
    ```

---

## Estructura del Proyecto

(La estructura del proyecto permanece igual que en la versión anterior del README)
```
.
├── cotizador/
│   └── ...
├── run.py
└── ...
```
