import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProyectoLogiCo.settings')
django.setup()

from django.contrib.auth.models import User
from App.models import UsuarioRol

def crear_usuarios():
    usuarios = [
        {'username': 'root', 'email': 'root@logico.com', 'password': 'Root123@', 'rol': 'admin'},
        {'username': 'admin', 'email': 'admin@logico.com', 'password': 'Admin123@', 'rol': 'admin'},
        {'username': 'recepcionista', 'email': 'recep@logico.com', 'password': 'Recep123@', 'rol': 'recepcionista'},
    ]
    
    for usuario in usuarios:
        if not User.objects.filter(username=usuario['username']).exists():
            user = User.objects.create_user(
                username=usuario['username'],
                email=usuario['email'],
                password=usuario['password']
            )
            UsuarioRol.objects.create(usuario=user, rol=usuario['rol'])
            print(f"✅ Usuario {usuario['username']} creado como {usuario['rol']}")
        else:
            print(f"⚠️ Usuario {usuario['username']} ya existe")

if __name__ == '__main__':
    crear_usuarios()