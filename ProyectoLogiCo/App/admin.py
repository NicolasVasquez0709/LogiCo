from django.contrib import admin
from .models import (
    Farmacia, Moto, Motorista, Movimiento,
    AsignacionMoto, AsignacionFarmacia, UsuarioRol,
    PasswordRecoveryCode, ReporteMovimiento
)

# Register your models here.

@admin.register(Farmacia)
class FarmaciaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'region', 'comuna', 'telefono']
    search_fields = ['nombre', 'correo']
    list_filter = ['region', 'comuna']

@admin.register(Moto)
class MotoAdmin(admin.ModelAdmin):
    list_display = ['patente', 'marca', 'modelo', 'anio', 'disponible']
    search_fields = ['patente', 'marca']
    list_filter = ['disponible', 'anio']

@admin.register(Motorista)
class MotoristaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'rut', 'licencia', 'estado', 'fecha_ingreso']
    search_fields = ['nombre', 'rut', 'correo']
    list_filter = ['estado', 'licencia']

@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'tipo', 'estado', 'fecha_registro', 'motorista']
    search_fields = ['codigo', 'tipo']
    list_filter = ['estado', 'tipo', 'fecha_registro']

@admin.register(AsignacionMoto)
class AsignacionMotoAdmin(admin.ModelAdmin):
    list_display = ['motorista', 'moto', 'fecha_asignacion', 'activa']
    list_filter = ['activa', 'fecha_asignacion']

@admin.register(AsignacionFarmacia)
class AsignacionFarmaciaAdmin(admin.ModelAdmin):
    list_display = ['motorista', 'farmacia', 'fecha_asignacion', 'activa']
    list_filter = ['activa', 'fecha_asignacion']

@admin.register(UsuarioRol)
class UsuarioRolAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'rol', 'activo', 'fecha_creacion']
    list_filter = ['rol', 'activo']

@admin.register(PasswordRecoveryCode)
class PasswordRecoveryCodeAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'is_used']
    list_filter = ['is_used', 'created_at']

@admin.register(ReporteMovimiento)
class ReporteMovimientoAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'fecha_generacion', 'generado_por', 'total_movimientos']
    list_filter = ['tipo', 'fecha_generacion']