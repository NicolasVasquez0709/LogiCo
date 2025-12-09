from django.apps import AppConfig
from django.db.models.signals import post_migrate

class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'App'

    def ready(self):
        """Se ejecuta automáticamente cuando Django inicia"""
        post_migrate.connect(create_default_users, sender=self)

def create_default_users(sender, **kwargs):
    """Crea usuarios por defecto después de las migraciones"""
    from django.contrib.auth.models import User
    from App.models import UsuarioRol
    
    try:
        # Crear usuario Admin
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_user(
                username='admin',
                email='admin@logico.com',
                password='Admin123@',
                is_staff=True,
                is_superuser=True
            )
            UsuarioRol.objects.create(usuario=admin_user, rol='admin')
            print("✅ Usuario admin creado: admin / Admin123@")

        # Crear usuario Recepcionista
        if not User.objects.filter(username='recepcionista').exists():
            recep_user = User.objects.create_user(
                username='recepcionista',
                email='recepcionista@logico.com',
                password='Recep123@'
            )
            UsuarioRol.objects.create(usuario=recep_user, rol='recepcionista')
            print("✅ Usuario recepcionista creado: recepcionista / Recep123@")
    except Exception as e:
        pass  # Silencia errores en desarrollo