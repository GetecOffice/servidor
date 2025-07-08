import sys
import os
import django
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Configuración de entorno
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Servidor.settings')
load_dotenv(os.path.join(BASE_DIR, '.env'))
django.setup()

from Aplicacion.models import Registro

# Variables de configuración
ALERTA_TIEMPO = 30  # segundos
ULTIMA_ACTUALIZACION = None
ALERTA_ENVIADA = False

# Datos de correo desde .env
EMAIL_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_PASS = os.getenv("EMAIL_HOST_PASS")
EMAIL_TO = os.getenv("EMAIL_TO")
SMTP_SERVER = os.getenv("EMAIL_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("EMAIL_PORT", 465))


def enviar_correo(asunto, mensaje_texto):
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = asunto
        msg["From"] = EMAIL_USER
        msg["To"] = EMAIL_TO

        # Mensaje HTML
        mensaje_html = f"""
        <html>
        <body>
            <h3>⚠️ Alerta de inactividad del servidor</h3>
            <p>No se ha detectado actividad en los últimos <strong>{ALERTA_TIEMPO} segundos</strong>.</p>
            <p><strong>Posibles causas:</strong></p>
            <ul>
                <li>🔌 <b>Servidor apagado:</b> Verifique que esté encendido.</li>
                <li>⏸️ <b>Servidor pausado:</b> El sistema podría estar detenido temporalmente.</li>
                <li>🛠️ <b>Programa detenido:</b> Contacte al técnico para una revisión remota.</li>
            </ul>
            <p style="font-size: 0.9em; color: gray;">Este mensaje fue generado automáticamente por el sistema de monitoreo.</p>
        </body>
        </html>
        """

        msg.attach(MIMEText(mensaje_texto, "plain"))
        msg.attach(MIMEText(mensaje_html, "html"))

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASS)
            smtp.send_message(msg)
        print("📧 Correo de alerta enviado correctamente")

    except Exception as e:
        print("❌ Error al enviar correo:", e)


def monitorear():
    global ULTIMA_ACTUALIZACION, ALERTA_ENVIADA

    while True:
        registro = Registro.objects.filter(estatus=1).first()
        if registro:
            registro.estatus = 2
            registro.save()
            print(f"✔ Actualizado: {registro.descripcion}")
            ULTIMA_ACTUALIZACION = time.time()
            ALERTA_ENVIADA = False
        else:
            print("Sin cambios")
            if ULTIMA_ACTUALIZACION:
                tiempo_sin_cambios = time.time() - ULTIMA_ACTUALIZACION
                if tiempo_sin_cambios > ALERTA_TIEMPO and not ALERTA_ENVIADA:
                    asunto = "⚠️ Alerta: El servidor no ha respondido"
                    mensaje_texto = (
                        f"No se ha detectado actividad del servidor en los últimos {ALERTA_TIEMPO} segundos.\n\n"
                        "Posibles causas:\n"
                        "• Servidor apagado\n"
                        "• Servidor en pausa\n"
                        "• Programa detenido\n\n"
                        "Este mensaje fue generado automáticamente."
                    )
                    enviar_correo(asunto, mensaje_texto)
                    ALERTA_ENVIADA = True
        time.sleep(10)


if __name__ == "__main__":
    monitorear()
