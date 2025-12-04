from django import forms
from .models import Farmacia, Moto, Motorista, AsignacionMoto, AsignacionFarmacia, Movimiento


class FarmaciaForm(forms.ModelForm):
    class Meta:
        model = Farmacia
        fields = ['nombre', 'direccion', 'telefono', 'correo', 'region', 'provincia', 'comuna']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'region': forms.Select(attrs={'class': 'form-select', 'id': 'region-select'}),
            'provincia': forms.Select(attrs={'class': 'form-select', 'id': 'provincia-select'}),
            'comuna': forms.Select(attrs={'class': 'form-select', 'id': 'comuna-select'}),
        }

class MotoForm(forms.ModelForm):
    class Meta:
        model = Moto
        fields = ['patente', 'marca', 'modelo', 'anio', 'disponible']
        widgets = {
            'patente': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'anio': forms.NumberInput(attrs={'class': 'form-control', 'min': 2000}),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# ===============================
# FORMULARIO MOTORISTA
# ===============================
class MotoristaForm(forms.ModelForm):
    class Meta:
        model = Motorista
        fields = ['nombre', 'rut', 'telefono', 'correo', 'licencia', 'estado', 'fecha_ingreso']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'licencia': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_ingreso': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        }



# ===============================
# FORMULARIOS DE ASIGNACIONES
# ===============================
class AsignacionMotoForm(forms.ModelForm):
    class Meta:
        model = AsignacionMoto
        fields = ['motorista', 'moto', 'fecha_fin', 'activa']
        widgets = {
            'motorista': forms.Select(attrs={'class': 'form-select'}),
            'moto': forms.Select(attrs={'class': 'form-select'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'activa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class AsignacionFarmaciaForm(forms.ModelForm):
    class Meta:
        model = AsignacionFarmacia
        fields = ['motorista', 'farmacia', 'fecha_fin', 'activa']
        widgets = {
            'motorista': forms.Select(attrs={'class': 'form-select'}),
            'farmacia': forms.Select(attrs={'class': 'form-select'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'activa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# ===============================
# FORMULARIO MOVIMIENTO
# ===============================
class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = [
            'codigo',  
            'tipo',        
            'descripcion',
            'estado',
            'farmacia_origen',
            'destino',
            'motorista',
            'moto'
        ]
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'farmacia_origen': forms.Select(attrs={'class': 'form-select'}),
            'destino': forms.TextInput(attrs={'placeholder': 'Ej: Calle 1234, Casa roja'}),
            'motorista': forms.Select(attrs={'class': 'form-select'}),
            'moto': forms.Select(attrs={'class': 'form-select'}),
        }