from flask import Flask, render_template, request, jsonify
import json
import os
import time
from whatsappHook import Whatsapp  # TODO: Implementar la clase Whatsapp al backend

ACTUAL_MESSAGE = ""

app = Flask(__name__, template_folder="../templates", static_folder="../static")
wppHandler = Whatsapp()

@app.route('/')
def index():
    print("Accediendo a la ruta '/'")
    return render_template("index.html")

@app.route('/send_message', methods=['POST'])
def send_message():
    print("Accediendo a la ruta '/send_message'")
    data = request.get_json()
    print(f"Datos recibidos: {data}")
    user_message = data.get('message', '')
    
    # Aqui ira la funcion para responder al usuario por whatsapp
    wppHandler.send_message(f"Mensaje enviado desde el server: {user_message}")
    
    # Devolver una respuesta
    print("Devolviendo respuesta JSON")
    return jsonify({"status": "success", "message": "Mensaje recibido"})

# Para gestionar recordatorios
def load_reminders():
    print("Cargando recordatorios...")
    if os.path.exists('./reminders.json'):
        print("El archivo reminders.json existe")
        with open('./reminders.json', 'r') as f:
            try:
                reminders = json.load(f)
                print(f"Recordatorios cargados: {reminders}")
                return reminders
            except Exception as e:
                print(f"Error al cargar reminders.json: {e}")
                return []
    else:
        print("El archivo reminders.json no existe")
    return []

def save_reminders(reminders):
    print("Guardando recordatorios...")
    with open('./reminders.json', 'w') as f:
        json.dump(reminders, f)
    print("Recordatorios guardados")

@app.route('/add_reminder', methods=['POST'])
def add_reminder():
    print("Accediendo a la ruta '/add_reminder'")
    data = request.get_json()
    print(f"Datos recibidos: {data}")
    
    reminder = {
        'subject': data.get('subject'),
        'description': data.get('description'),
        'datetime': data.get('datetime')
    }
    
    reminders = load_reminders()
    reminders.append(reminder)
    save_reminders(reminders)
    
    print("Recordatorio agregado")
    return jsonify({"status": "success", "message": "Recordatorio agregado"})

@app.route('/delete_reminder', methods=['POST'])
def delete_reminder():
    print("Accediendo a la ruta '/delete_reminder'")
    data = request.get_json()
    print(f"Datos recibidos: {data}")
    subject = data.get('subject')
    datetime = data.get('datetime')
    
    reminders = load_reminders()
    reminders = [r for r in reminders if not (r['subject'] == subject and r['datetime'] == datetime)]
    save_reminders(reminders)
    
    print("Recordatorio eliminado")
    return jsonify({"status": "success", "message": "Recordatorio eliminado"})

@app.route('/get_reminders')
def get_reminders():
    print("Accediendo a la ruta '/get_reminders'")
    reminders = load_reminders()
    print(f"Recordatorios obtenidos: {reminders}")
    return jsonify({"status": "success", "reminders": reminders})

if __name__ == '__main__':
    print("Iniciando la aplicación...")
    try:
        print("Intentando iniciar sesión en WhatsApp...")
        wppHandler.login()
    except Exception as e:
        print(f"Error al iniciar sesión en WhatsApp: {e}")
    
    while wppHandler.is_logged_in != True:
        print("Esperando a que el usuario inicie sesión en WhatsApp...")
        time.sleep(1)

    time.sleep(2)
    
    try:
        print("Abriendo grupo..")
        wppHandler.openGroup("2° MS anti-dictadura")
    except Exception as e:
        print(f"Error al abrir el grupo: {e}")

    try:
        print("Iniciando el servidor Flask...")
        app.run()
    except Exception as e:
        print(f"Error al iniciar el servidor Flask: {e}")