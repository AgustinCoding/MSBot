from flask import Flask, render_template, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import json
import os
import atexit
import time
from whatsapphook import Whatsapp 
from gptmodel import GPTmodel


app = Flask(__name__, template_folder="../templates", static_folder="../static")
wppHandler = Whatsapp()
gpt = GPTmodel(api="AIzaSyDNAOdKegeCp_RQU7DVZs83XNtazj8iO44")
scheduler = BackgroundScheduler()



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

    try:
        response = gpt.generate_response(user_prompt=user_message)

        wppHandler.send_message(f"""NUEVA SOLICITUD: {user_message}
    ------------------------------------------
    MSBot: {response}
    """)
    except Exception as e:
        print(f"Error al citar al modelo: {e}")
    
    # Devolver una respuesta
    print("Devolviendo respuesta JSON")
    return jsonify({"status": "success", "message": "Mensaje recibido"})

# Para gestionar recordatorios
def save_reminders(reminders):
    print("Guardando recordatorios...")
    with open('reminders.json', 'w') as f:
        json.dump(reminders, f)
    print("Recordatorios guardados")


def schedule_reminders():
    print("Enviando recordatorios")
    try:
        send_reminders()
    except Exception as e:
        print("Error al enviar recordatorios", e)

def load_reminders():
    print("Cargando recordatorios...")

    # Obtener la ruta absoluta del archivo JSON
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "reminders.json")  

    if os.path.exists(file_path):
        print(f"El archivo {file_path} existe.")
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                reminders = json.load(f)
                format_date()
                print(f"Recordatorios cargados: {reminders}")
                return reminders
            except Exception as e:
                print(f"Error al cargar reminders.json: {e}")
                return []
    else:
        print(f"El archivo {file_path} no existe.")
        return []
    
def format_date():

    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "reminders.json")  

    if os.path.exists(file_path):
        print("Reminders.json encontrado para formatear")
        try:
            with open(file_path, "r", encoding="UTF-8") as f:
                reminders = json.load(f)

            for reminder in reminders:
                if 'datetime' in reminder:
                    reminder['datetime'] = reminder['datetime'].replace("T", " ")

            with open(file_path, "w", encoding= "UTF-8") as f:
                json.dump(reminders, f, indent=2)
                print("JSON Formateado correctamente")
        except:
            print("Error al formatear archivo")
    else:
        print("Archivo no encontrado")

    

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

@app.route('/send_reminders')
def send_reminders():
    reminder_message = f"--------RECORDATORIOS----------"
    try:
        reminders = load_reminders()
        x=1
        for reminder in reminders:
            reminder_message+= f"\n{x}-{reminder['subject']} : {reminder['description']} | Vence: {reminder['datetime']}\n"
            x+=1

        print(reminder_message)
        try:
            wppHandler.send_message(reminder_message)
        except:
            print("Mensaje no enviado")
    except:
        print("No hay recordatorios")


scheduler.add_job(schedule_reminders, 'interval', hours=3)
scheduler.start()

atexit.register(lambda: scheduler.shutdown(wait=False))

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
