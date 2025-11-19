const searchInput = document.getElementById("searchInput");
const searchResults = document.getElementById("searchResults");

let timeout = null;

if (searchInput) {
    searchInput.addEventListener("input", () => {
        clearTimeout(timeout);

        timeout = setTimeout(() => {
            const q = searchInput.value.trim();

            if (q === "") {
                searchResults.innerHTML = "";
                searchResults.classList.remove("show");
                return;
            }

            fetch(`/products/search_products/?q=${encodeURIComponent(q)}`)
                .then(res => {
                    if (!res.ok) throw new Error("Error en la búsqueda");
                    return res.json();
                })
                .then(data => {
                    searchResults.innerHTML = data.html;
                    searchResults.classList.add("show");
                })
                .catch(err => {
                    console.error("Error en búsqueda AJAX:", err);
                    searchResults.innerHTML = `
                        <div class="list-group-item text-danger">
                            Error al buscar
                        </div>`;
                    searchResults.classList.add("show");
                });
        }, 300);
    });
}

// cerrar dropdown al hacer click afuera
document.addEventListener("click", function (event) {
    if (!searchInput || !searchResults) return;

    const isClickInside =
        searchInput.contains(event.target) ||
        searchResults.contains(event.target);

    if (!isClickInside) {
        searchResults.innerHTML = "";
        searchResults.classList.remove("show");
    }
});
