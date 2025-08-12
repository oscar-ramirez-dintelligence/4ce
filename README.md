# Cotizador de Medios Publicitarios (Refactorizado)

Una aplicación web construida con Flask y Google Cloud Firestore para gestionar soportes publicitarios, clientes y cotizaciones. Esta versión ha sido **refactorizada** para seguir las mejores prácticas de Flask, utilizando el patrón **Application Factory** y **Blueprints** para una estructura modular, escalable y mantenible.

## Características Principales

- **Arquitectura Modular**: Código organizado en Blueprints (`main`, `soportes`, `cotizaciones`, `api`) y una capa de servicios.
- **Gestión de Soportes**: Operaciones CRUD para soportes publicitarios.
- **Catálogo Paginado**: Visualización de soportes con paginación del lado del servidor.
- **Integración con Google Maps**: Visualización de la ubicación de los soportes en un mapa interactivo.
- **Gestión de Cotizaciones**: Creación y visualización de cotizaciones para clientes.
- **Sesiones Seguras**: Uso de cookies firmadas por el servidor para la gestión de sesiones.
- **Script de Seeding**: Incluye un script para poblar la base de datos con datos de prueba.

## Arquitectura

- **Framework Backend**: Flask (con patrón Application Factory y Blueprints)
- **Capa de Lógica de Negocio**: Servicios (`cotizador/services/`)
- **Base de Datos**: Google Cloud Firestore (NoSQL)
- **Framework Frontend**: Bootstrap 5
- **Renderizado de Plantillas**: Jinja2
- **Servidor de Producción**: Gunicorn

---

## Guía de Instalación y Ejecución

### 1. Prerrequisitos

- Python 3.13 o superior.
- `pip` y `venv`.
- Una cuenta de Google Cloud con un proyecto activo y las APIs (`Firestore`, `Maps JavaScript`) habilitadas.

### 2. Configuración de Credenciales

1.  **Clave de API de Google Maps**: Créala en la consola de Google Cloud y guárdala.
2.  **Cuenta de Servicio para Firestore**:
    - Crea una cuenta de servicio con el rol **Editor de Cloud Datastore**.
    - Descarga la clave en formato **JSON**.
    - Renombra el archivo a `service-account-key.json` y colócalo en la raíz del proyecto.

### 3. Configuración del Entorno Local

1.  **Clonar el Repositorio** y navegar al directorio.

2.  **Crear y Activar un Entorno Virtual**:
    ```bash
    python3 -m venv venv && source venv/bin/activate
    ```

3.  **Instalar Dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar Variables de Entorno**:
    - Crea una copia de `.env.example` y renómbrala a `.env`.
    - Rellena las variables con tus claves y credenciales:
      ```ini
      SECRET_KEY="tu_clave_secreta_aqui"
      GOOGLE_APPLICATION_CREDENTIALS="./service-account-key.json"
      GOOGLE_MAPS_API_KEY="tu_google_maps_api_key_aqui"
      ```

### 4. Poblar la Base de Datos (Seeding)

Ejecuta el script de seeding dentro del contexto de la aplicación para poblar Firestore:
```bash
python seed_data.py
```

### 5. Ejecutar la Aplicación

**A. Modo de Desarrollo:**
El `run.py` está configurado para usar las variables de entorno y ejecutar la app en modo de depuración.
```bash
# Simplemente ejecuta el script
python run.py

# O usando el CLI de Flask
flask --app run.py run
```
La aplicación estará disponible en `http://127.0.0.1:5000` por defecto.

**B. Modo de Producción (para Cloud Run):**
Usa Gunicorn para apuntar a la application factory.
```bash
gunicorn 'cotizador:create_app()' --bind 0.0.0.0:8080
```

---

## Estructura del Proyecto Refactorizado

```
.
├── cotizador/                # Paquete principal de la aplicación
│   ├── __init__.py           # Application Factory (create_app)
│   ├── db.py                 # Lógica de conexión a la base de datos
│   ├── api/                  # Blueprint para la API RESTful
│   │   └── routes.py
│   ├── cotizaciones/         # Blueprint para las rutas de cotizaciones
│   │   └── routes.py
│   ├── main/                 # Blueprint para rutas principales (home, login)
│   │   └── routes.py
│   ├── servicios/            # Lógica de negocio
│   │   ├── cotizacion_service.py
│   │   ├── soporte_service.py
│   │   └── tipos_cliente_service.py
│   ├── soportes/             # Blueprint para las rutas de soportes
│   │   └── routes.py
│   ├── static/               # Archivos estáticos (CSS, JS)
│   │   └── css/
│   │       └── style.css
│   └── templates/            # Plantillas Jinja2
│       ├── base.html
│       └── ...
├── run.py                    # Punto de entrada para ejecutar la aplicación
├── seed_data.py              # Script para poblar la base de datos
├── requirements.txt
├── .env.example
└── .gitignore
```
