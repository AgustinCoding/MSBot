
// Datos de materias y horarios (estáticos)
const horariosMaterias = {
    "Matemáticas": { dia: "Lunes", hora: "10:00 AM" },
    "Física": { dia: "Miércoles", hora: "09:00 AM" },
    "Inglés": { dia: "Martes", hora: "11:00 AM" },
    "Historia": { dia: "Jueves", hora: "02:00 PM" },
    "Biología": { dia: "Viernes", hora: "08:00 AM" },
    "Química": { dia: "Lunes", hora: "12:00 PM" },
    "Literatura": { dia: "Martes", hora: "09:00 AM" }
};

// Llenar el selector de materias
document.addEventListener('DOMContentLoaded', function() {
    const subjectSelect = document.getElementById('subject');
    
    for (const materia in horariosMaterias) {
        const option = document.createElement('option');
        option.value = materia;
        option.textContent = `${materia} (${horariosMaterias[materia].dia}, ${horariosMaterias[materia].hora})`;
        subjectSelect.appendChild(option);
    }

    // Navegación por pestañas
    const tabButtons = document.querySelectorAll('.tab-button');
    const sections = document.querySelectorAll('.section');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabId = button.getAttribute('data-tab');
            
            // Desactivar todas las pestañas y secciones
            tabButtons.forEach(btn => btn.classList.remove('active'));
            sections.forEach(section => section.classList.remove('active'));
            
            // Activar la pestaña y sección seleccionada
            button.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        });
    });

    // Manejo del formulario de mensajes
    const messageForm = document.getElementById('message-form');
    const chatMessages = document.getElementById('chat-messages');
    const userMessageInput = document.getElementById('user-message');

    messageForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const userMessage = userMessageInput.value.trim();
        
        if (userMessage) {
            // Agregar mensaje del usuario al chat
            addMessage(userMessage, 'user-message');
            
            // Aquí enviaríamos la pregunta a un backend para procesarla
            // y enviarla al grupo de WhatsApp
            // En un caso real, esta parte sería una llamada AJAX a tu backend
            
            // Simulamos la confirmación de envío
            setTimeout(() => {
                // Mensaje de confirmación
                const confirmationMessage = "Tu pregunta ha sido enviada y será respondida en el grupo de WhatsApp de 2° MS con el formato: \"Nueva consulta: " + userMessage + "; [respuesta]\"";
                
                addMessage(confirmationMessage, 'bot-message');
                showNotification('Pregunta enviada al grupo de WhatsApp');
            }, 1000);
            
            // Limpiar el campo de entrada
            userMessageInput.value = '';
        }
    });

    // Función para agregar mensajes al chat
    function addMessage(text, className) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${className}`;
        
        const messagePara = document.createElement('p');
        messagePara.textContent = text;
        
        messageDiv.appendChild(messagePara);
        chatMessages.appendChild(messageDiv);
        
        // Auto-scroll al último mensaje
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Manejo del formulario de recordatorios
    const reminderForm = document.getElementById('reminder-form');
    const remindersList = document.getElementById('reminders-list');

    reminderForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const subject = document.getElementById('subject').value;
        const description = document.getElementById('reminder-description').value;
        const datetime = document.getElementById('reminder-datetime').value;
        
        if (subject && description && datetime) {
            // Crear y agregar el recordatorio a la lista
            addReminder(subject, description, datetime);
            
            // Mostrar notificación
            showNotification('Recordatorio agregado con éxito');
            
            // Limpiar el formulario
            document.getElementById('reminder-description').value = '';
            document.getElementById('reminder-datetime').value = '';
        }
    });

    // Función para agregar recordatorios
    function addReminder(subject, description, datetime) {
        const reminderItem = document.createElement('li');
        reminderItem.className = 'reminder-item';
        
        const date = new Date(datetime);
        const formattedDate = date.toLocaleDateString('es-ES', { 
            weekday: 'long', 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
        
        reminderItem.innerHTML = `
            <div class="reminder-content">
                <h4>${subject}</h4>
                <p>${description}</p>
                <p class="reminder-date">${formattedDate}</p>
            </div>
            <button class="delete-reminder">×</button>
        `;
        
        // Agregar evento para eliminar el recordatorio
        const deleteButton = reminderItem.querySelector('.delete-reminder');
        deleteButton.addEventListener('click', function() {
            reminderItem.remove();
            showNotification('Recordatorio eliminado');
        });
        
        remindersList.appendChild(reminderItem);
        
        // En un caso real, aquí iría la lógica para programar el envío al WhatsApp
        // simulateWhatsAppReminder(subject, description, datetime);
    }

    // Sistema de notificaciones
    const notification = document.getElementById('notification');
    const notificationMessage = document.getElementById('notification-message');
    const closeNotification = document.getElementById('close-notification');
    
    function showNotification(message) {
        notificationMessage.textContent = message;
        notification.classList.remove('hidden');
        
        // Ocultar automáticamente después de 3 segundos
        setTimeout(() => {
            notification.classList.add('hidden');
        }, 3000);
    }
    
    closeNotification.addEventListener('click', function() {
        notification.classList.add('hidden');
    });
});