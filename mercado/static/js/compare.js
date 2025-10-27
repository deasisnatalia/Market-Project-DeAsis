document.addEventListener('DOMContentLoaded', function() {
    // Habilitar/deshabilitar boton de comparar
    const checkboxes = document.querySelectorAll('.compare-checkbox');
    const compareBtn = document.getElementById('compare-btn');

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const checked = document.querySelectorAll('.compare-checkbox:checked');
            compareBtn.disabled = checked.length < 2;;
        });
    });

    // Accion del boton de comparar
    compareBtn.addEventListener('click', function() {
        const selectedCheckboxes = document.querySelectorAll('.compare-checkbox:checked');
        const selectedIds = Array.from(selectedCheckboxes).map(cb => cb.value);

        if (selectedIds.length < 2) {
            alert('Debe seleccionar al menos 2 productos para comparar');
            return;
        }

        // Obtener datos de los productos seleccionados
        const selectedProducts = [];
        selectedIds.forEach(id => {
            const card = document.querySelector(`.compare-checkbox[value="${id}"]`).closest('.card');
            const name = card.querySelector('.card-title').textContent.trim();
            const price = card.querySelector('.card-text strong').textContent.trim();
            const description = card.querySelector('.card-text').textContent.trim().split('\n')[1] || 'Sin descripción';
            const imageSrc = card.querySelector('img') ? card.querySelector('img').src : null;

            selectedProducts.push({
                id: id,
                name: name,
                price: price,
                description: description,
                image: imageSrc
            });
        });

        // Mostrar modal con tabla de comparación
        showComparisonModal(selectedProducts);
    });

    function showComparisonModal(products) {
        // Crear el HTML del modal
        let tableRows = '';
        products.forEach(product => {
            tableRows += `
                <tr>
                    <td>${product.name}</td>
                    <td>${product.price}</td>
                </tr>
            `;
        });

        const modalHtml = `
            <div class="modal fade" id="comparisonModal" tabindex="-1" aria-labelledby="comparisonModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="comparisonModalLabel">Comparación de Productos</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <div class="table-responsive" style="max-height: 60vh; overflow-y: auto;">
                                <table class="table table-striped">
                                    <thead class="sticky-top bg-white">
                                        <tr>
                                            <th>Nombre</th>
                                            <th>Precio</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        ${tableRows}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Agregar el modal al body
        document.body.insertAdjacentHTML('beforeend', modalHtml);

        // Mostrar el modal
        const modalElement = document.getElementById('comparisonModal');
        const modal = new bootstrap.Modal(modalElement);
        modal.show();

        // Eliminar el modal del DOM cuando se cierre
        modalElement.addEventListener('hidden.bs.modal', function () {
            modalElement.remove();
        });
    }
});