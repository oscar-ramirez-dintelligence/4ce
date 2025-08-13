# Cotizador de Medios Publicitarios (Refactorizado)

Una aplicación web construida con Flask y Google Cloud Firestore para gestionar soportes publicitarios, clientes y cotizaciones. Esta versión ha sido **refactorizada** para seguir las mejores prácticas de Flask, utilizando el patrón **Application Factory** y **Blueprints** para una estructura modular, escalable y mantenible.

## Autenticación con Google Cloud

Esta aplicación utiliza **Application Default Credentials (ADC)** para autenticarse con los servicios de Google Cloud (Firestore). Esto significa que **no es necesario** gestionar archivos de clave de cuenta de servicio (`.json`) manualmente. La autenticación se maneja automáticamente según el entorno:

-   **En Desarrollo Local**: La aplicación usará las credenciales de tu usuario de `gcloud`.
-   **En Cloud Run**: La aplicación usará la cuenta de servicio asociada a la instancia de Cloud Run.

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
    -   Rellena las variables:
        ```ini
        # Genera una clave segura con: python -c 'import secrets; print(secrets.token_hex(24))'
        SECRET_KEY="tu_clave_secreta_aqui"

        # La clave de API de Google Maps que creaste.
        GOOGLE_MAPS_API_KEY="tu_google_maps_api_key_aqui"
        ```

### 4. Poblar la Base de Datos (Seeding)

Ejecuta el script de seeding para poblar Firestore con datos de prueba:
```bash
python seed_data.py
```

### 5. Ejecutar la Aplicación

**A. Modo de Desarrollo:**
```bash
flask --app run.py run
```
La aplicación estará disponible en `http://127.0.0.1:5000`.

**B. Modo de Producción (para Cloud Run):**
-   Asegúrate de que la cuenta de servicio de tu instancia de Cloud Run tenga el rol de **Editor de Cloud Datastore** (o un rol más restrictivo con los permisos necesarios para Firestore).
-   Despliega la aplicación. Gunicorn se iniciará con el siguiente comando:
    ```bash
    gunicorn 'cotizador:create_app()' --bind 0.0.0.0:8080
    ```

---

## Estructura del Proyecto

```
.
├── cotizador/
│   ├── __init__.py
│   ├── db.py
│   ├── api/
│   ├── cotizaciones/
│   ├── main/
│   ├── servicios/
│   ├── soportes/
│   ├── static/
│   └── templates/
├── run.py
├── seed_data.py
├── requirements.txt
├── .env.example
└── .gitignore
```
