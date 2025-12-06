from django.db import models
from django.contrib.auth.models import User


def es_admin(user):
    """Verifica si el usuario es admin"""
    try:
        return user.rol.rol == 'admin'
    except UsuarioRol.DoesNotExist:
        return False


def es_recepcionista(user):
    """Verifica si el usuario es recepcionista"""
    try:
        return user.rol.rol == 'recepcionista'
    except UsuarioRol.DoesNotExist:
        return False


def es_admin_o_recepcionista(user):
    """Verifica si es admin o recepcionista"""
    try:
        return user.rol.rol in ['admin', 'recepcionista']
    except UsuarioRol.DoesNotExist:
        return False


# =====================================================
# AUTENTICACIÓN

class UsuarioRol(models.Model):
    """Modelo para asignar roles a los usuarios"""
    
    ROLES = [
        ('admin', 'Administrador'),
        ('recepcionista', 'Recepcionista'),
    ]
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='rol')
    rol = models.CharField(max_length=20, choices=ROLES, default='recepcionista')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.usuario.username} - {self.get_rol_display()}"
    
    class Meta:
        db_table = 'usuario_rol'
        verbose_name = 'Rol de Usuario'
        verbose_name_plural = 'Roles de Usuarios'

class Farmacia(models.Model):
    REGIONES = [
        ("Arica y Parinacota", "Arica y Parinacota"),
        ("Tarapacá", "Tarapacá"),
        ("Antofagasta", "Antofagasta"),
        ("Atacama", "Atacama"),
        ("Coquimbo", "Coquimbo"),
        ("Valparaíso", "Valparaíso"),
        ("Metropolitana de Santiago", "Metropolitana de Santiago"),
        ("Libertador General Bernardo O'Higgins", "Libertador General Bernardo O'Higgins"),
        ("Maule", "Maule"),
        ("Ñuble", "Ñuble"),
        ("Biobío", "Biobío"),
        ("La Araucanía", "La Araucanía"),
        ("Los Ríos", "Los Ríos"),
        ("Los Lagos", "Los Lagos"),
        ("Aysén del General Carlos Ibáñez del Campo", "Aysén del General Carlos Ibáñez del Campo"),
        ("Magallanes y de la Antártica Chilena", "Magallanes y de la Antártica Chilena"),
    ]

    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField(max_length=100)
    region = models.CharField(max_length=100, choices=REGIONES)
    provincia = models.CharField(max_length=100)
    comuna = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} ({self.comuna})"

    class Meta:
        db_table = 'farmacia'
        verbose_name = 'Farmacia'
        verbose_name_plural = 'Farmacias'


class Moto(models.Model):
    patente = models.CharField(max_length=10, unique=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    anio = models.PositiveIntegerField(db_column="anio", verbose_name="año")
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.marca} {self.modelo} - {self.patente}"

    class Meta:
        db_table = 'moto'


class Motorista(models.Model):
    LICENCIA_OPCIONES = [
        ('C1', 'Clase C1'),
        ('C2', 'Clase C2'),
        ('C3', 'Clase C3'),
    ]

    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField(max_length=100)
    licencia = models.CharField(max_length=20, choices=LICENCIA_OPCIONES)
    estado = models.CharField(max_length=20, default='Activo')
    fecha_ingreso = models.DateField()
    farmacia = models.ForeignKey('Farmacia', on_delete=models.SET_NULL, null=True, blank=True)
    moto = models.ForeignKey('Moto', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.licencia})"

    class Meta:
        db_table = 'motorista'


# ==========================
# ASIGNACIONES
# ==========================

class AsignacionMoto(models.Model):
    motorista = models.ForeignKey(Motorista, on_delete=models.CASCADE)
    moto = models.ForeignKey(Moto, on_delete=models.CASCADE)
    fecha_asignacion = models.DateField(auto_now_add=True)
    fecha_fin = models.DateField(null=True, blank=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.motorista} ↔ {self.moto}"

    class Meta:
        db_table = 'asignacion_moto'


class AsignacionFarmacia(models.Model):
    motorista = models.ForeignKey(Motorista, on_delete=models.CASCADE)
    farmacia = models.ForeignKey(Farmacia, on_delete=models.CASCADE)
    fecha_asignacion = models.DateField(auto_now_add=True)
    fecha_fin = models.DateField(null=True, blank=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.motorista} ↔ {self.farmacia}"

    class Meta:
        db_table = 'asignacion_farmacia'

# ==========================
# MOVIMIENTOS (Release 2)
# ==========================

class Movimiento(models.Model):
    TIPO_MOVIMIENTO = [
        ('DIRECTO', 'Movimiento Directo'),
        ('RECETA', 'Movimiento con Receta'),
        ('TRASLADO', 'Movimiento con Traslado'),
        ('REENVIO', 'Movimiento con Reenvío'),
    ]

    ESTADO_MOVIMIENTO = [
        ('EN_PROCESO', 'En proceso'),
        ('COMPLETADO', 'Completado'),
        ('ANULADO', 'Anulado'),
    ]

    codigo = models.CharField(max_length=20, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPO_MOVIMIENTO)
    descripcion = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    estado = models.CharField(max_length=20, choices=ESTADO_MOVIMIENTO, default='EN_PROCESO')
    farmacia_origen = models.ForeignKey(Farmacia, on_delete=models.SET_NULL, null=True, related_name='movimientos_origen')
    destino = models.CharField(max_length=200)
    motorista = models.ForeignKey(Motorista, on_delete=models.SET_NULL, null=True)
    moto = models.ForeignKey(Moto, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.codigo} - {self.tipo}"

    class Meta:
        db_table = 'movimiento'
        ordering = ['-fecha_registro']

# ==========================
# REPORTES
# ==========================

class ReporteMovimiento(models.Model):
    TIPO_REPORTE = [
        ('DIARIO', 'Reporte Diario'),
        ('MENSUAL', 'Reporte Mensual'),
        ('ANUAL', 'Reporte Anual'),
    ]

    tipo = models.CharField(max_length=10, choices=TIPO_REPORTE)
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    generado_por = models.CharField(max_length=100)
    total_movimientos = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.tipo} - {self.fecha_generacion.date()}"

    class Meta:
        db_table = 'reporte_movimiento'
