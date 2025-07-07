import sys
import os
import django
import time

# Ruta base del proyecto (ajusta si es necesario)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Servidor.settings')
django.setup()

from Aplicacion.models import Registro

def monitorear():
    while True:
        registro = Registro.objects.filter(estatus=1).first()
        if registro:
            registro.estatus = 2
            registro.save()
            print(f"✔ Actualizado: {registro.descripcion}")
        else:
            print("Sin cambios")
        time.sleep(10)

if __name__ == "__main__":
    monitorear()
