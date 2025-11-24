document.addEventListener('DOMContentLoaded', function () {

    //Funcion para cargar datos del producto en el modal de editar
    function loadEditModalData(productId) {
        console.log("Cargando datos para editar producto ID:", productId);
        const editButton = document.querySelector(`button[data-pk="${productId}"]`);
        console.log("Boton encontrado:", editButton);
        if (!productId) {
            console.error("ID de producto no definido para edicion");
            return;
        }
        if (isNaN(productId) || productId === '') {
            console.error("ID de producto inválido:", productId);
            return;
        }

        console.log("Cargando datos para editar producto ID:", productId);
        if (editButton) {
            const name = editButton.getAttribute('data-name');
            const price = editButton.getAttribute('data-price');
            const description = editButton.getAttribute('data-description');
            const stock = editButton.getAttribute('data-stock');
            const image = editButton.getAttribute('data-image');

            console.log("Datos obtenidos:", {name, price, description, stock, image});
            
            document.getElementById('edit_name').value = name;
            document.getElementById('edit_price').value = parseFloat(price).toFixed(2);
            document.getElementById('edit_description').value = description;
            document.getElementById('edit_stock').value = stock;
            document.getElementById('edit-product-id').value = productId;

            const currentImageDiv = document.getElementById('current-image-edit');
            if (image) {
                currentImageDiv.innerHTML = `<img src="${image}" alt="Imagen actual" style="width: 50px; height: 50px; object-fit: cover; margin-top: 5px;">`;
            } else {
                currentImageDiv.innerHTML = '<span class="text-muted">Sin imagen actual</span>';
            }

            //Actualiza la acción del formulario para apuntar a la URL
            if (productId) {
                document.getElementById('edit-product-form').action = window.MyApp.urls.editProductPattern.replace('0', productId);
            } else {
                console.error("No se pudo establecer la acción del formulario: ID del producto es inválido:", productId);
                return;
            }
            const editModal = new bootstrap.Modal(document.getElementById('editModal'));
            editModal.show();
        } else {
            console.log("No se encontro el boton de edicion para el producto ID:", productId);
        }
    }

    //Eventos de botones de editar al cargar la pagina
    function assignEditEvents() {
        const editButtons = document.querySelectorAll('.open-edit-modal');

        editButtons.forEach(button => {
            const newButton = button.cloneNode(true);
            button.parentNode.replaceChild(newButton, button);

            newButton.addEventListener('click', function() {
                const productId = this.getAttribute('data-pk');
                if (productId && productId !== "undefined") {
                    loadEditModalData(productId);
                }
            });
        });
    }

    // Asigna eventos iniciales
    assignEditEvents();

    // formulario de crear
    const createForm = document.getElementById('create-product-form');
    if (createForm) { 
        console.log("Formulario de creacion encontrado");
        createForm.addEventListener('submit', function(e) {
            e.preventDefault();
            console.log("Formulario de creacion interceptado"); 
            const url = window.MyApp.urls.createProduct;
            const formData = new FormData(this);
            const errorsDiv = document.getElementById('create-form-errors');

            //Valida y formatear el precio
            const priceInput = document.getElementById('id_price');
            let priceValue = priceInput.value.trim();
            if (priceValue === '') {
                errorsDiv.classList.remove('d-none');
                errorsDiv.innerHTML = '<p>El precio no puede estar vacío.</p>';
                return;
            }

            //reemplaza coma por punto
            priceValue = priceValue.replace(',', '.');
            
            const priceNum = parseFloat(priceValue);
            if (isNaN(priceNum) || priceNum < 0) {
                errorsDiv.classList.remove('d-none');
                errorsDiv.innerHTML = '<p>El precio debe ser un número positivo.</p>';
                return;
            }

            //formatea el precio a 2 decimales y reemplaza en el formData
            formData.set('price', priceNum.toFixed(2));
            console.log("URL de creación:", window.MyApp.urls.createProduct);
            if (!window.MyApp.urls.createProduct) {
                console.error("La URL de creación no está definida.");
                return;
            }
            fetch(window.MyApp.urls.createProduct, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
            })
            .then((response) => response.json())
            .then((data) => {
                if (data.success) {
                    console.log("Creacion eitosa, actualizando lista...");
                    assignEditEvents();

                    const modal = bootstrap.Modal.getInstance(document.getElementById("createModal"));
                    modal.hide();
                    createForm.reset();
                } else {
                    const errorDiv = document.getElementById("create-form-errors");
                    errorDiv.classList.remove("d-none");
                    errorDiv.innerHTML = data.error;
                }
            })
            .catch(error => {
                console.error(error);
            });
        });
    }

    //Formulario de edicion
    const editForm = document.getElementById('edit-product-form');
    if (editForm) {
        console.log("Formulario de edicion encontrado");
        editForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const formData = new FormData(this);
            const productId = document.getElementById('edit-product-id').value;
            const errorsDiv = document.getElementById('edit-form-errors');

            //valida y formatea el precio
            const priceInput = document.getElementById('edit_price');
            let priceValue = priceInput.value.trim();
            if (priceValue === '') {
                errorsDiv.classList.remove('d-none');
                errorsDiv.innerHTML = '<p>El precio no puede estar vacío.</p>';
                return;
            }

            priceValue = priceValue.replace(',', '.');
            const priceNum = parseFloat(priceValue);
            if (isNaN(priceNum) || priceNum < 0) {
                errorsDiv.classList.remove('d-none');
                errorsDiv.innerHTML = '<p>El precio debe ser un número positivo.</p>';
                return;
            }

            formData.set('price', priceNum.toFixed(2));

            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const modalElement = document.getElementById('editModal');
                    const modal = bootstrap.Modal.getInstance(modalElement);
                    if (modal) modal.hide();
                    
                    if (data.html) {
                        document.getElementById('products-list-container').innerHTML = data.html;
                    }
                    alert(data.message || 'Producto actualizado correctamente');
                    
                    assignEditEvents();
                } else {
                    errorsDiv.classList.remove('d-none');
                    errorsDiv.innerHTML = '<ul></ul>';
                    const ul = errorsDiv.querySelector('ul');
                    try {
                        const errors = JSON.parse(data.errors);
                        for (const field in errors) {
                            errors[field].forEach(error => {
                                const li = document.createElement('li');
                                li.textContent = `${field}: ${error}`;
                                ul.appendChild(li);
                            });
                        }
                    } catch (e) {
                        errorsDiv.innerHTML = '<p>Error al procesar los datos.</p>';
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                errorsDiv.classList.remove('d-none');
                errorsDiv.innerHTML = '<p>Error al procesar la solicitud.</p>';
            });
        });
    }

});