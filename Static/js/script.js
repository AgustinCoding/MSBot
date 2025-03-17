// Datos de materias y horarios (estaticos)
const horariosMaterias = {
    "SISTEMAS OPERATIVOS": [
        { dia: "Miércoles", hora: "12:25 PM", salon: "107", profesor: "Dall'oglio, Pamela" },
        { dia: "Miércoles", hora: "13:55 PM", salon: "Laboratorio 3", profesor: "Dall'oglio, Pamela" }
    ],
    "LEGISLACIÓN": { dia: "Jueves", hora: "12:25 PM", salon: "EP2", profesor: "Suárez, Agustina" },
    "HISTORIA ECONÓMICA": { dia: "Viernes", hora: "12:25 PM", salon: "206", profesor: "Varela, Alicia" },
    "ANÁLISIS Y PRODUCCIÓN DE TEXTOS": [
        { dia: "Lunes", hora: "13:10 PM", salon: "202", profesor: "Martínez, Mónica" },
        { dia: "Viernes", hora: "14:40 PM", salon: "206", profesor: "Martínez, Mónica" }
    ],
    "PROGRAMACIÓN AVANZADA": { dia: "Martes", hora: "13:55 PM", salon: "Laboratorio 1", profesor: "De león, Jorge" },
    "MATEMÁTICA": [
        { dia: "Jueves", hora: "13:55 PM", salon: "205", profesor: "Flores, Luis" },
        { dia: "Viernes", hora: "15:35 PM", salon: "205", profesor: "Flores, Luis" }
    ],
    "MATEMÁTICA CTS": { dia: "Lunes", hora: "15:35 PM", salon: "202", profesor: "Antunez, Jorge" },
    "INGLÉS": [
        { dia: "Jueves", hora: "15:35 PM", salon: "205", profesor: "Mujica, Lourdes" },
        { dia: "Viernes", hora: "17:05 PM", salon: "206", profesor: "Mujica, Lourdes" }
    ],
    "REDES INFORMÁTICAS": { dia: "Martes", hora: "16:20 PM", salon: "Taller TMII", profesor: "Zunin Leonardo" },
    "INTRODUCCIÓN BASE DE DATOS": { dia: "Miércoles", hora: "16:20 PM", salon: "Laboratorio 3", profesor: "Dall'oglio, Pamela" },
    "AC VIDEOJUEGOS": { dia: "Lunes", hora: "17:05 PM", salon: "Laboratorio 2", profesor: "" }
};

// funcion para ejecutar cuando el documento este cargado
document.addEventListener('DOMContentLoaded', function() {
    // Llenar el selector de materias
    fillSubjectSelect();
    
    // Configurar eventos para el formulario de mensajes
    setupMessageForm();
    
    // Configurar eventos para el formulario de recordatorios
    setupReminderForm();
    
    // Configurar sistema de notificaciones
    setupNotifications();
    
    // Cargar recordatorios existentes
    loadExistingReminders();
    
    // Configurar navegacion por pestañas
    setupTabNavigation();
});

// Llenar el selector de materias
function fillSubjectSelect() {
    const subjectSelect = document.getElementById('subject');
    
    for (const materia in horariosMaterias) {
        const option = document.createElement('option');
        option.value = materia;
        
        if (Array.isArray(horariosMaterias[materia])) {
            // Para materias con múltiples horarios
            let infoText = `${materia} (`;
            horariosMaterias[materia].forEach((horario, index) => {
                infoText += `${horario.dia} ${horario.hora}, Salón ${horario.salon}`;
                if (index < horariosMaterias[materia].length - 1) infoText += " | ";
            });
            infoText += ")";
            option.textContent = infoText;
        } else {
            // Para materias con un solo horario
            option.textContent = `${materia} (${horariosMaterias[materia].dia}, ${horariosMaterias[materia].hora}, Salón ${horariosMaterias[materia].salon})`;
        }
        
        subjectSelect.appendChild(option);
    }
}

// Configurar navegacion por pestañas
function setupTabNavigation() {
    const tabButtons = document.querySelectorAll('.tab-button');
    const sections = document.querySelectorAll('.section');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabId = button.getAttribute('data-tab');
            
            // Desactivar todas las pestañas y secciones
            tabButtons.forEach(btn => btn.classList.remove('active'));
            sections.forEach(section => section.classList.remove('active'));
            
            // Activar la pestaña y seccion seleccionada
            button.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        });
    });
}

// Configurar formulario de mensajes
function setupMessageForm() {
    const messageForm = document.getElementById('message-form');
    const chatMessages = document.getElementById('chat-messages');
    const userMessageInput = document.getElementById('user-message');

    messageForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const userMessage = userMessageInput.value.trim();
        
        if (userMessage) {
            // Agregar mensaje del usuario al chat
            addMessage(userMessage, 'user-message');
            
            // Enviar mensaje al backend Flask usando fetch
            fetch('/send_message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: userMessage })
            })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
                
                // Mensaje de confirmacion
                const confirmationMessage = "Tu pregunta ha sido enviada y será respondida en el grupo de WhatsApp de 2° MS con el formato: \"Nueva consulta: " + userMessage + "; [respuesta]\"";
                
                addMessage(confirmationMessage, 'bot-message');
                showNotification('Pregunta enviada al grupo de WhatsApp');
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Error al enviar la pregunta', true);
            });
            
            // Limpiar el campo de entrada
            userMessageInput.value = '';
        }
    });
}

// Funcion para agregar mensajes al chat
function addMessage(text, className) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${className}`;
    
    const messagePara = document.createElement('p');
    messagePara.textContent = text;
    
    messageDiv.appendChild(messagePara);
    chatMessages.appendChild(messageDiv);
    
    // Auto-scroll al ultimo mensaje
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Configurar formulario de recordatorios
function setupReminderForm() {
    const reminderForm = document.getElementById('reminder-form');
    
    reminderForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const subject = document.getElementById('subject').value;
        const description = document.getElementById('reminder-description').value;
        const datetime = document.getElementById('reminder-datetime').value;
        
        if (subject && description && datetime) {
            // Enviar recordatorio al backend Flask
            fetch('/add_reminder', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    subject: subject,
                    description: description, 
                    datetime: datetime 
                })
            })
            .then(response => response.json())
            .then(data => {
                console.log('Reminder added:', data);
                
                // Crear y agregar el recordatorio a la lista
                addReminder(subject, description, datetime);
                
                // Mostrar notificación
                showNotification('Recordatorio agregado con éxito');
                
                // Limpiar el formulario
                document.getElementById('reminder-description').value = '';
                document.getElementById('reminder-datetime').value = '';
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Error al agregar el recordatorio', true);
            });
        }
    });
}

// Funcion para agregar recordatorios
function addReminder(subject, description, datetime) {
    const remindersList = document.getElementById('reminders-list');
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
        <button class="delete-reminder" data-datetime="${datetime}">×</button>
    `;
    
    // Agregar evento para eliminar el recordatorio
    const deleteButton = reminderItem.querySelector('.delete-reminder');
    deleteButton.addEventListener('click', function() {
        const reminderDatetime = this.getAttribute('data-datetime');
        
        // Eliminar el recordatorio del backend
        fetch('/delete_reminder', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                subject: subject,
                datetime: reminderDatetime 
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Reminder deleted:', data);
            reminderItem.remove();
            showNotification('Recordatorio eliminado');
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Error al eliminar el recordatorio', true);
        });
    });
    
    remindersList.appendChild(reminderItem);
}

// Configurar sistema de notificaciones
function setupNotifications() {
    const notification = document.getElementById('notification');
    const closeNotification = document.getElementById('close-notification');
    
    closeNotification.addEventListener('click', function() {
        notification.classList.add('hidden');
    });
}

// Funcion para mostrar notificaciones
function showNotification(message, isError = false) {
    const notification = document.getElementById('notification');
    const notificationMessage = document.getElementById('notification-message');
    
    notificationMessage.textContent = message;
    notification.classList.remove('hidden');
    
    if (isError) {
        notification.classList.add('error');
    } else {
        notification.classList.remove('error');
    }
    
    // Ocultar automaticamente despues de 3 segundos
    setTimeout(() => {
        notification.classList.add('hidden');
    }, 3000);
}

// Cargar recordatorios existentes
function loadExistingReminders() {
    fetch('/get_reminders')
        .then(response => response.json())
        .then(data => {
            console.log('Reminders loaded:', data);
            if (data.reminders && data.reminders.length > 0) {
                data.reminders.forEach(reminder => {
                    addReminder(reminder.subject, reminder.description, reminder.datetime);
                });
            }
        })
        .catch(error => {
            console.error('Error loading reminders:', error);
        });
}