from django.db.models.signals import post_migrate
from django.contrib.auth.models import User
from django.dispatch import receiver
from App.models import UsuarioRol

@receiver(post_migrate)
def crear_usuarios_por_defecto(sender, **kwargs):
    if sender.name != 'App':
        return

    usuarios_por_defecto = [
        {
            'username': 'root',
            'email': 'root@logico.com',
            'password': 'Root123@',
            'rol': 'admin',
        },
        {
            'username': 'admin',
            'email': 'admin@logico.com',
            'password': 'Admin123@',
            'rol': 'admin',
        },
        {
            'username': 'recepcionista',
            'email': 'recep@logico.com',
            'password': 'Recep123@',
            'rol': 'recepcionista',
        },
    ]

    for u in usuarios_por_defecto:
        if not User.objects.filter(username=u['username']).exists():
            user = User.objects.create_user(
                username=u['username'],
                email=u['email'],
                password=u['password']
            )
            UsuarioRol.objects.create(user=user, rol=u['rol'])
            print(f"✔ Usuario creado: {u['username']}")
