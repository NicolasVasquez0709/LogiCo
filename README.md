Se debe configurar la base de datos en settings.py, donde se debe cambiar el nombre de la base de datos y la constraseña:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'proyectointegrado',
        'USER': 'root',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
    }
}
Instalaciones necesarias para funcionamiento del codigo:
1. pip install django
2. pip install reportlab
3. pip install mysqlclient
