# scripts/cargar_usuarios.py

import os
import django
import sys
import csv
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'institucion_backend.settings')
django.setup()

from django.contrib.auth.models import User
from academico.models import Usuario, Rector, Coordinador, Docente, Estudiante
from academico.models import Sede, Grupo  


def crear_usuario(row):
    tipo_usuario = row['tipo_usuario'].lower()
    num_doc = row['numero_documento']
    password = num_doc  
    username = num_doc

    # 1. Crear usuario base (User)
    if User.objects.filter(username=username).exists():
        print(f"Usuario {username} ya existe, se omite.")
        return

    user = User.objects.create_user(
        username=username,
        password=password,
        email=row['correo']
    )

    # Agregar nombres y apellidos a auth_user
    user.first_name = row['nombres']
    user.last_name = row['apellidos']
    user.save()

    # 2. Crear modelo Usuario
    usuario = Usuario.objects.create(user=user, tipo_usr=tipo_usuario)

    # 3. Datos comunes
    try:
        fecha_nacimiento = datetime.strptime(row['fecha_nacimiento'], '%d/%m/%Y').date()
    except ValueError:
        print(f"Fecha inválida para {username}: {row['fecha_nacimiento']}")
        return

    datos_comunes = {
        'tipo_documento': row['tipo_documento'],
        'numero_documento': num_doc,
        'nombres': row['nombres'],
        'apellidos': row['apellidos'],
        'sexo': row['sexo'],
        'telefono': row['telefono'],
        'correo': row['correo'],
        'direccion': row['direccion'],
        'fecha_nacimiento': fecha_nacimiento,
        'estado': row['estado'],
        'usuario': usuario,
    }

    # 4. Crear modelo según tipo de usuario
    if tipo_usuario == 'rector':
        sede = Sede.objects.filter(codigo_dane=row['sede_id']).first() if row.get('sede_id') else None
        Rector.objects.create(**datos_comunes, sede=sede)
    elif tipo_usuario == 'coordinador':
        Coordinador.objects.create(**datos_comunes)
    elif tipo_usuario == 'docente':
        Docente.objects.create(**datos_comunes)
    elif tipo_usuario == 'estudiante':
        grupo = Grupo.objects.filter(id=row['grupo_id']).first() if row.get('grupo_id') else None
        Estudiante.objects.create(**datos_comunes, grupo=grupo)
    else:
        print(f"Tipo de usuario no reconocido: {tipo_usuario}")

    print(f"Usuario {username} creado correctamente.")

def cargar_csv():
    ruta = 'scripts/usuariosMasivoss.csv'
    with open(ruta, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        print("Encabezados del CSV:", reader.fieldnames)
        for row in reader:
            if not row or 'tipo_usuario' not in row or not row['tipo_usuario']:
                print("Fila ignorada por estar vacía o mal formada:", row)
                continue
            crear_usuario(row)


if __name__ == '__main__':
    cargar_csv()
