# Efra Cerraduras

Efra Cerraduras es una aplicación web desarrollada con Django que permite la gestión integral de productos, clientes, pedidos y presupuestos dentro de una plataforma comercial.

El sistema incorpora funcionalidades de comercio electrónico, administración de usuarios, generación de presupuestos en PDF, gestión de pedidos y comunicación en tiempo real mediante WebSockets.

## Características Principales

### Gestión de Usuarios

* Registro e inicio de sesión.
* Modelo de usuario personalizado.
* Gestión de perfiles con imagen y datos adicionales.
* Control de permisos y roles.

### Gestión de Productos

* Alta, baja, modificación y consulta de productos.
* Gestión de stock.
* Carga de imágenes.
* Administración de categorías.

### Carrito de Compras

* Agregar y eliminar productos.
* Modificación de cantidades.
* Validación automática de stock.
* Cálculo dinámico de subtotales y totales.

### Gestión de Pedidos

* Creación de pedidos a partir del carrito.
* Seguimiento de estados:

  * Pendiente
  * En Proceso
  * Completado
  * Rechazado
* Historial de pedidos por cliente.

### Presupuestos

* Generación automática de presupuestos.
* Exportación en formato PDF mediante ReportLab.

### Panel Administrativo

* Administración de clientes.
* Administración de productos.
* Administración de pedidos.
* Visualización de información comercial.

### API REST

* Endpoints para gestión de productos.
* Serialización de datos mediante Django REST Framework.
* Arquitectura preparada para integración con aplicaciones externas.

### Comunicación en Tiempo Real

* Implementación de WebSockets mediante Django Channels.
* Actualización de información en tiempo real.

## Tecnologías Utilizadas

### Backend

* Python
* Django
* Django REST Framework
* Django Channels

### Frontend

* HTML5
* CSS3
* JavaScript
* Bootstrap

### Base de Datos

* SQLite (desarrollo)

### Librerías Adicionales

* ReportLab
* Pillow

### Herramientas

* Git
* GitHub
* Virtual Environment (venv)

## Instalación

### 1. Clonar repositorio

```bash
git clone https://github.com/deasisnatalia/Market-Project-DeAsis.git
cd Market-Project-DeAsis/mercado
```

### 2. Crear entorno virtual

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar migraciones

```bash
python manage.py migrate
```

### 5. Crear superusuario

```bash
python manage.py createsuperuser
```

### 6. Configurar variables de entorno

Crear archivo `.env`:

```env
SECRET_KEY=tu_clave_secreta
DEBUG=True
```

### 7. Ejecutar servidor

```bash
python manage.py runserver
```

Acceder desde:

```text
http://127.0.0.1:8000/
```

## Aprendizajes del Proyecto

Durante el desarrollo de este proyecto se trabajó con:

* Arquitectura MVC de Django.
* Desarrollo de APIs REST.
* Autenticación y autorización de usuarios.
* Manejo de relaciones entre modelos.
* Generación de documentos PDF.
* Comunicación en tiempo real mediante WebSockets.
* Gestión de archivos multimedia.
* Control de versiones con Git y GitHub.

## Autor

Natalia Ximena De Asis

GitHub:
https://github.com/deasisnatalia
