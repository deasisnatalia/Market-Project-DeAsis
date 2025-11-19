// --- Modal del carrito ---
document.addEventListener('DOMContentLoaded', function() {
    fetchCartCount();

    const cartModalElement = document.getElementById('cartModal');
    if (cartModalElement) {
        cartModalElement.addEventListener('shown.bs.modal', function () {
            console.log("Modal abierto, cargando contenido...");
            fetchCartContents();
        });
    }

    // --- Funcion para cargar el contenido del carrito ---
    function fetchCartContents() {
        console.log("Fetch a la vista del carrito iniciado...");
        fetch(window.MyApp.urls.viewCart)
            .then(response => {
                console.log("Respuesta recibida:", response.status);
                return response.text();
            })
            .then(html => {
                console.log("HTML recibido (primeros 200 chars):", html.substring(0, 200));
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');

                const cartContentDivFromServer = doc.getElementById('cart-items-content');
                const cartContentContainer = document.getElementById('cart-items-content');

                if (!cartContentContainer) {
                    console.error("No existe en el DOM local el elemento con id 'cart-items-content'. Asegurate de tenerlo en el modal.");
                    return;
                }

                if (cartContentDivFromServer) {
                    cartContentContainer.innerHTML = cartContentDivFromServer.innerHTML;
                    console.log("Contenido del carrito actualizado en el DOM.");

                    cartContentContainer.querySelectorAll('.update-quantity-btn').forEach(button => {
                        button.replaceWith(button.cloneNode(true));
                    });
                    cartContentContainer.querySelectorAll('.update-quantity-btn').forEach(button => {
                        button.addEventListener('click', function() {
                            const change = parseInt(this.getAttribute('data-change'), 10);
                            const itemEl = this.closest('[data-item-id]');
                            if (!itemEl) return;
                            const itemId = itemEl.getAttribute('data-item-id');
                            updateQuantity(itemId, change);
                        });
                    });

                    cartContentContainer.querySelectorAll('.remove-item-btn').forEach(button => {
                        button.replaceWith(button.cloneNode(true));
                    });
                    cartContentContainer.querySelectorAll('.remove-item-btn').forEach(button => {
                        button.addEventListener('click', function() {
                            const itemEl = this.closest('[data-item-id]');
                            if (!itemEl) return;
                            const itemId = itemEl.getAttribute('data-item-id');
                            removeFromCart(itemId);
                        });
                    });

                    // --- Habilitar/Deshabilitar botones '+' según stock
                    cartContentContainer.querySelectorAll('[data-item-id]').forEach(itemDiv => {
                        const stock = parseInt(itemDiv.getAttribute('data-product-stock') || '0', 10);
                        const quantityDisplay = itemDiv.querySelector('.quantity-display');
                        const plusButton = itemDiv.querySelector('.update-quantity-btn[data-change="1"]');

                        if (quantityDisplay && plusButton) {
                            const currentQuantity = parseInt(quantityDisplay.textContent || '0', 10);

                            if (currentQuantity >= stock) {
                                plusButton.disabled = true;
                                plusButton.classList.add('btn-secondary');
                                plusButton.classList.remove('btn-outline-secondary');
                                plusButton.textContent = '=';
                            } else {
                                plusButton.disabled = false;
                                plusButton.classList.add('btn-outline-secondary');
                                plusButton.classList.remove('btn-secondary');
                                plusButton.textContent = '+';
                            }
                        }
                    });

                } else {
                    cartContentContainer.innerHTML = '<p class="text-center">No se pudo cargar el contenido del carrito.</p>';
                    console.error("No se encontró el elemento con id 'cart-items-content' dentro del HTML recibido desde el servidor.");
                }
            }).catch(error => {
                console.error('Error al cargar el contenido del carrito:', error);
                const cartContentContainer = document.getElementById('cart-items-content');
                if (cartContentContainer) {
                    cartContentContainer.innerHTML = '<p class="text-danger">Error al cargar el carrito.</p>';
                }
            });
    }

    // --- Funcion para actualizar la cantidad de un producto ---
    function updateQuantity(itemId, change) {
        const url = window.MyApp.urls.updateCartItem.replace("__ID__", itemId);

        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ quantity_change: change })
        })
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return response.json();
        })
        .then(data => {
            if (!data.success) {
                alert(data.error || "Ocurrió un error al actualizar la cantidad.");
                return;
            }
            const newQty = Number(data.new_quantity ?? 0);
            const container = document.getElementById('cart-items-content');
            if (!container) {
                fetchCartContents();
                fetchCartCount();
                return;
            }
            const itemDiv = container.querySelector(`[data-item-id="${itemId}"]`);
            if (!itemDiv) {
                fetchCartContents();
                fetchCartCount();
                return;
            }
            if (newQty === 0) {
                fetchCartContents();
                fetchCartCount();
                return;
            }
            const quantityDisplay = itemDiv.querySelector('.quantity-display');
            if (quantityDisplay) quantityDisplay.textContent = newQty;
            const unitPrice = parseFloat(itemDiv.getAttribute('data-product-price'));
            const itemTotalPriceSpan = itemDiv.querySelector('.item-total-price');
            if (itemTotalPriceSpan && !isNaN(unitPrice)) {
                itemTotalPriceSpan.textContent = `$${(unitPrice * newQty).toFixed(2)}`;
            }
            
            // Actualizar boton -
            const minusButton = itemDiv.querySelector('.update-quantity-btn[data-change="-1"]');
            if (minusButton) {
                minusButton.disabled = newQty <= 1;
                minusButton.classList.toggle('btn-secondary', newQty <= 1);
                minusButton.classList.toggle('btn-outline-secondary', newQty > 1);
                minusButton.textContent = newQty <= 1 ? '=' : '-';
            }
            // Actualizar botón +
            const plusButton = itemDiv.querySelector('.update-quantity-btn[data-change="1"]');
            const stock = Number(data.product_stock ?? itemDiv.getAttribute('data-product-stock'));
            if (plusButton) {
                plusButton.disabled = newQty >= stock;
                plusButton.classList.toggle('btn-secondary', newQty >= stock);
                plusButton.classList.toggle('btn-outline-secondary', newQty < stock);
                plusButton.textContent = newQty >= stock ? '=' : '+';
            }

            // Actualizamos subtotal global y contador
            const subtotalAmountElement = document.getElementById('cart-subtotal-amount');
            if (subtotalAmountElement && typeof data.new_total !== 'undefined') {
                subtotalAmountElement.textContent = `$${Number(data.new_total).toFixed(2)}`;
            }

            fetchCartCount();
        })
        .catch(error => {
            console.error('Error al actualizar la cantidad del ítem:', error);
            alert("Ocurrió un error al actualizar la cantidad. Por favor, inténtalo de nuevo.");
            fetchCartContents();
        });
    }

    // --- Funcion para eliminar un item  ---
    function removeFromCart(itemId) {
        const url = window.MyApp.urls.removeFromCart ? window.MyApp.urls.removeFromCart.replace("__ID__", itemId) : `/products/remove-from-cart/${itemId}/`;
        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            }
        })
        .then(response => {
            if (response.ok) {
                fetchCartContents();
                fetchCartCount();
            } else {
                console.error("Error en removeFromCart, status:", response.status);
            }
        }).catch(error => {
            console.error('Error al eliminar ítem del carrito:', error);
        });
    }

    // --- Contador del carrito ---
    function fetchCartCount() {
        fetch(window.MyApp.urls.cartCount, {
            credentials: "include"
        })
        .then(response => response.json())
        .then(data => {
            const el = document.getElementById('cart-count');
            if (el) el.textContent = data.count;
        })
        .catch(error => {
            console.error('Error al cargar el conteo del carrito:', error);
        });
    }

    // --- Checkout ---
    function checkoutMercadoPago() {
        console.log("Iniciando checkout de Mercado Pago...");
        fetch(window.MyApp.urls.createPreference, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                'Content-Type': 'application/json',
            },
        })
        .then(response => {
            console.log("Respuesta de create_preference recibida:", response.status);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return response.json();
        })
        .then(data => {
            console.log("Datos de preferencia recibidos:", data);
            if (data.init_point) {
                window.location.href = data.init_point;
            } else {
                alert(data.error || "Ocurrió un error al iniciar el pago.");
            }
        })
        .catch(error => {
            console.error('Error al iniciar el checkout:', error);
            alert("Ocurrió un error al iniciar el pago. Por favor, inténtalo de nuevo.");
        });
    }

    const checkoutBtn = document.getElementById('checkout-btn');
    if (checkoutBtn) checkoutBtn.addEventListener('click', checkoutMercadoPago);
});

// --- generarPDF  ---
function generarPDF() {
    fetch('/budgets/generar-presupuesto/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
    })
    .then(response => {
        if (response.ok) return response.blob();
        throw new Error("Error al generar PDF");
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'presupuesto.pdf';
        a.click();
    })
    .catch(error => console.error("Error:", error));
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
