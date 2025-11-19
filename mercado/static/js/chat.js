document.addEventListener('DOMContentLoaded', function () {
    const chatBtn = document.getElementById('chat-btn');
    const chatModal = new bootstrap.Modal(document.getElementById('chatModal'));
    const chatMessages = document.getElementById('chat-messages');
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');

    if (chatBtn) {
        chatBtn.addEventListener('click', () => {
            chatModal.show();
        });
    }

    if (sendBtn) {
        sendBtn.addEventListener('click', enviarMensaje);
    }

    if (chatInput) {
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') enviarMensaje();
        });
    }

    function enviarMensaje() {
        const mensaje = chatInput.value.trim();
        if (!mensaje) return;

        chatMessages.innerHTML += `
            <div class="d-flex justify-content-end mb-2">
                <div class="p-2 rounded bg-primary text-white" style="max-width: 75%;">
                    ${mensaje}
                </div>
            </div>
        `;
        chatInput.value = '';

        // Mostrar indicador de "escribiendo..."
        const typingId = 'typing';
        chatMessages.innerHTML += `
            <div id="${typingId}" class="d-flex justify-content-start mb-2">
                <div class="p-2 rounded bg-light border" style="max-width: 75%;">
                    <em>IA está escribiendo...</em>
                </div>
            </div>
        `;
        chatMessages.scrollTop = chatMessages.scrollHeight;

        // Enviar al backend
        fetch(window.CHAT_API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: 'mensaje=' + encodeURIComponent(mensaje)
        })
        .then(response => response.json())
        .then(data => {
            // Eliminar el mensaje de "escribiendo..."
            document.getElementById(typingId)?.remove();

            // Mostrar la respuesta de la IA
            chatMessages.innerHTML += `
                <div class="d-flex justify-content-start mb-2">
                    <div class="p-2 rounded bg-light border" style="max-width: 75%;">
                        ${data.respuesta}
                    </div>
                </div>
            `;
            chatMessages.scrollTop = chatMessages.scrollHeight;
        })
        .catch(error => {
            document.getElementById(typingId)?.remove();
            chatMessages.innerHTML += `
                <div class="alert alert-danger">Error: No se pudo conectar con la IA.</div>
            `;
        });
    }

    // Función para obtener CSRF token
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

});