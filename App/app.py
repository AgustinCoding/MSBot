from flask import Flask, render_template, request, jsonify
import json
import os
from whatsappHook import Whatsapp #TODO: Implementar la clase Whatsapp al backend



app = Flask(__name__, template_folder="../templates", static_folder="../static")

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    user_message = data.get('message', '')
    
    # Aqui ira la funcion para responder al usuario por whatsapp
    print(f"Mensaje recibido: {user_message}")
    
    # Devolver una respuesta
    return jsonify({"status": "success", "message": "Mensaje recibido"})

# Para gestionar recordatorios
def load_reminders():
    if os.path.exists('./reminders.json'):
        with open('./reminders.json', 'r') as f:
            try:
                return json.load(f)
            except:
                return []
    return []

def save_reminders(reminders):
    with open('./reminders.json', 'w') as f:
        json.dump(reminders, f)

@app.route('/add_reminder', methods=['POST'])
def add_reminder():
    data = request.get_json()
    
    reminder = {
        'subject': data.get('subject'),
        'description': data.get('description'),
        'datetime': data.get('datetime')
    }
    
    reminders = load_reminders()
    reminders.append(reminder)
    save_reminders(reminders)
    
    return jsonify({"status": "success", "message": "Recordatorio agregado"})

@app.route('/delete_reminder', methods=['POST'])
def delete_reminder():
    data = request.get_json()
    subject = data.get('subject')
    datetime = data.get('datetime')
    
    reminders = load_reminders()
    reminders = [r for r in reminders if not (r['subject'] == subject and r['datetime'] == datetime)]
    save_reminders(reminders)
    
    return jsonify({"status": "success", "message": "Recordatorio eliminado"})

@app.route('/get_reminders')
def get_reminders():
    reminders = load_reminders()
    return jsonify({"status": "success", "reminders": reminders})

if __name__ == '__main__':
    app.run(debug=True)