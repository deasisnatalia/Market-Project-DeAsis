# Michi Mercado

**Michi Mercado** es una aplicación web desarrollada en **Django** que simula una plataforma de comercio electrónico. Permite a los usuarios navegar productos, gestionar un carrito de compras con funcionalidades de agregar, quitar y ajustar cantidades según el stock disponible, y realizar pagos a través de **Mercado Pago**. Además, incluye un CRUD completo para que los usuarios gestionen sus propios productos.

## Características

*   **Autenticación de Usuarios:** Registro e inicio de sesión.
*   **Gestión de Productos:** CRUD (Crear, Leer, Actualizar, Eliminar) de productos por parte del usuario logueado.
*   **Catálogo de Productos:** Visualización de productos disponibles.
*   **Carrito de Compras Dinámico:**
    *   Agregar, quitar y ajustar cantidades de productos.
    *   Validación de stock disponible.
    *   Modal interno para visualizar y gestionar el carrito.
    *   Contador de ítems en el navbar (solo para usuarios logueados).
*   **Integración con Mercado Pago:** Procesamiento seguro de pagos.
*   **Interfaz de Usuario Responsiva:** Utiliza **Bootstrap** para una experiencia adaptable.
*   **Paginación:** En la vista de "Mis Productos".

## Tecnologías Utilizadas

*   **Backend:** [Python](https://www.python.org/) 3.x, [Django](https://www.djangoproject.com/)
*   **Frontend:** [HTML5](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5), [CSS3](https://developer.mozilla.org/en-US/docs/Web/CSS), [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript), [Bootstrap](https://getbootstrap.com/)
*   **Base de Datos:** [PostgreSQL]
*   **API de Pago:** [Mercado Pago](https://www.mercadopago.com.ar/developers/)
*   **Herramientas:** `pip`, `venv`

## Instalación Local (para desarrollo)

1.  **Clonar el repositorio:**

    ```bash
    git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
    cd TU_REPOSITORIO
    ```

2.  **Crear y activar un entorno virtual:**

    ```bash
    python -m venv venv
    # En Windows:
    venv\Scripts\activate
    ```

3.  **Instalar dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar la base de datos:**

    ```bash
    python manage.py migrate
    ```

5.  **Crear un superusuario (opcional):**

    ```bash
    python manage.py createsuperuser
    ```

6.  **Configurar variables de entorno:**
    *   Crea un archivo `.env` en la raíz del proyecto (mismo nivel que `manage.py`).
    *   Agrega tu `SECRET_KEY` y `MERCADOPAGO_ACCESS_TOKEN`:

        ```env
        SECRET_KEY=tu_clave_secreta_segura
        MERCADOPAGO_ACCESS_TOKEN=tu_access_token_de_mercadopago
        ```

7.  **Ejecutar el servidor de desarrollo:**

    ```bash
    python manage.py runserver
    ```

8.  **Abrir el navegador** en `http://127.0.0.1:8000/`.

## Autor
Natalia De Asis
