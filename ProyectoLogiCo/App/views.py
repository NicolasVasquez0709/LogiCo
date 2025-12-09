from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from datetime import timedelta

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from .models import (
    Employee, Farmacia, Moto, Motorista, Movimiento, 
    AsignacionMoto, AsignacionFarmacia, ReporteMovimiento, UsuarioRol,
    PasswordRecoveryCode
)
from .forms import (
    FarmaciaForm, MotoForm, MotoristaForm, 
    MovimientoForm, AsignacionMotoForm, AsignacionFarmaciaForm
)

from rest_framework.decorators import api_view
from rest_framework.response import Response
#=====================================================
# DECORADORES PERSONALIZADOS
# =====================================================





# =====================================================
# API REST VIEWSETS
# =====================================================

from rest_framework import serializers, viewsets

# SERIALIZERS
class FarmaciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmacia
        fields = '__all__'

class MotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moto
        fields = '__all__'

class MotoristaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motorista
        fields = '__all__'

class MovimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimiento
        fields = '__all__'

# VIEWSETS
class FarmaciaViewSet(viewsets.ModelViewSet):
    queryset = Farmacia.objects.all()
    serializer_class = FarmaciaSerializer

class MotoViewSet(viewsets.ModelViewSet):
    queryset = Moto.objects.all()
    serializer_class = MotoSerializer

class MotoristaViewSet(viewsets.ModelViewSet):
    queryset = Motorista.objects.all()
    serializer_class = MotoristaSerializer

class MovimientoViewSet(viewsets.ModelViewSet):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer

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
# =====================================================

def paginaPrincipal(request):
    """Página principal sin autenticación"""
    return render(request, 'paginaPrincipal.html')


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            try:
                rol = user.rol.rol
                if rol == 'admin':
                    return redirect('index')
                elif rol == 'recepcionista':
                    return redirect('index2')
            except UsuarioRol.DoesNotExist:
                # Si no tiene rol asignado, ir a página principal
                return redirect('paginaPrincipal')
        else:
            messages.error(request, '❌ Usuario o contraseña incorrectos.')
    
    return render(request, 'login.html')


@login_required(login_url='login')
@user_passes_test(es_admin)
def index(request):
    """Dashboard principal - Solo ADMIN"""
    return render(request, 'index.html')


@login_required(login_url='login')
@user_passes_test(es_recepcionista)
def index2(request):
    """Dashboard recepcionista - Solo RECEPCIONISTA"""
    return render(request, 'index2.html')

@login_required(login_url='login')
def logout_view(request):
    """Cerrar sesión"""
    logout(request)
    messages.success(request, '🚪 Sesión cerrada correctamente.')
    return redirect('paginaPrincipal')


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def cambiar_password(request):
    """Cambiar contraseña del usuario actual"""
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        
        user = request.user
        
        if not user.check_password(old_password):
            messages.error(request, '❌ La contraseña actual es incorrecta.')
            return redirect('index')
        
        if new_password1 != new_password2:
            messages.error(request, '❌ Las nuevas contraseñas no coinciden.')
            return redirect('index')
        
        if len(new_password1) < 8:
            messages.error(request, '❌ La contraseña debe tener al menos 8 caracteres.')
            return redirect('index')
        
        user.set_password(new_password1)
        user.save()
        login(request, user)
        messages.success(request, '✅ Contraseña actualizada correctamente.')
        return redirect('index')
    
    return render(request, 'cambiar_password.html')


# =====================================================
# RECUPERACIÓN DE CONTRASEÑA CON CÓDIGO
# =====================================================


@require_http_methods(["GET", "POST"])
def recuperar_password(request):
    """Enviar código de recuperación por email"""
    if request.method == "POST":
        email = request.POST.get('email', '').strip()
        
        try:
            user = User.objects.get(email=email)
            
            # Elimina código anterior
            PasswordRecoveryCode.objects.filter(user=user).delete()
            
            # Crea nuevo código
            recovery = PasswordRecoveryCode.objects.create(user=user)
            
            # Envía email simple
            asunto = "Tu código de recuperación - LogiCo"
            mensaje = f"Tu código es: {recovery.code}\n\nExpira en 15 minutos."
            
            send_mail(
                asunto,
                mensaje,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            
            messages.success(request, f"✔ Código enviado a {email}")
            return redirect('verificar_codigo')
            
        except User.DoesNotExist:
            messages.error(request, "❌ Email no encontrado")
    
    return render(request, 'recuperar_password.html')

@require_http_methods(["GET", "POST"])
def verificar_codigo(request):
    """Verificar código de recuperación"""
    if request.method == "POST":
        email = request.POST.get('email', '').strip()
        codigo = request.POST.get('codigo', '').strip().upper()
        
        try:
            user = User.objects.get(email=email)
            recovery = PasswordRecoveryCode.objects.get(user=user)
            
            if not recovery.is_valid():
                messages.error(request, "❌ El código ha expirado. Solicita uno nuevo.")
                return redirect('recuperar_password')
            
            if recovery.code != codigo:
                messages.error(request, "❌ Código incorrecto.")
                return render(request, 'verificar_codigo.html', {'email': email})
            
            # Código válido, redirige a cambiar contraseña
            request.session['recovery_email'] = email
            request.session['codigo_verificado'] = True
            messages.success(request, "✔ Código verificado. Establece tu nueva contraseña.")
            return redirect('cambiar_password_recuperacion')
        
        except User.DoesNotExist:
            messages.error(request, "❌ Email no encontrado.")
        except PasswordRecoveryCode.DoesNotExist:
            messages.error(request, "❌ Solicita un código primero.")
    
    return render(request, 'verificar_codigo.html')


@require_http_methods(["GET", "POST"])
def cambiar_password_recuperacion(request):
    """Cambiar contraseña después de verificar código"""
    if not request.session.get('codigo_verificado'):
        messages.error(request, "❌ Debes verificar el código primero.")
        return redirect('recuperar_password')
    
    if request.method == "POST":
        email = request.session.get('recovery_email')
        password1 = request.POST.get('password1', '').strip()
        password2 = request.POST.get('password2', '').strip()
        
        if len(password1) < 8:
            messages.error(request, "❌ La contraseña debe tener al menos 8 caracteres.")
        elif password1 != password2:
            messages.error(request, "❌ Las contraseñas no coinciden.")
        else:
            try:
                user = User.objects.get(email=email)
                user.set_password(password1)
                user.save()
                
                # Marca código como usado
                recovery = PasswordRecoveryCode.objects.get(user=user)
                recovery.is_used = True
                recovery.save()
                
                # Limpia sesión
                del request.session['recovery_email']
                del request.session['codigo_verificado']
                
                messages.success(request, "✔ Contraseña actualizada correctamente. Inicia sesión.")
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, "❌ Error al actualizar contraseña.")
    
    return render(request, 'cambiar_password_recuperacion.html')


@require_http_methods(["GET", "POST"])
def reset_password_confirm(request, uidb64, token):
    """Confirmar y cambiar contraseña desde enlace de email (LEGACY)"""
    from django.contrib.auth.tokens import default_token_generator
    from django.utils.http import urlsafe_base64_decode
    
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, '❌ El enlace de recuperación es inválido o ha expirado.')
        return redirect('paginaPrincipal')
    
    if not default_token_generator.check_token(user, token):
        messages.error(request, '❌ El enlace de recuperación ha expirado.')
        return redirect('paginaPrincipal')
    
    if request.method == 'POST':
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        
        if new_password1 != new_password2:
            messages.error(request, '❌ Las contraseñas no coinciden.')
            return redirect(request.path)
        
        if len(new_password1) < 8:
            messages.error(request, '❌ La contraseña debe tener al menos 8 caracteres.')
            return redirect(request.path)
        
        user.set_password(new_password1)
        user.save()
        messages.success(request, '✅ Contraseña actualizada. Ya puedes iniciar sesión.')
        return redirect('login')
    
    return render(request, 'reset_password_confirm.html', {'user': user})


@require_http_methods(["GET", "POST"])
def registrar_view(request):
    """Registro de nuevos usuarios como recepcionista"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, '❌ Este usuario ya existe.')
            return redirect('registrar')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, '❌ Este email ya está registrado.')
            return redirect('registrar')
        
        if password1 != password2:
            messages.error(request, '❌ Las contraseñas no coinciden.')
            return redirect('registrar')
        
        if len(password1) < 8:
            messages.error(request, '❌ La contraseña debe tener al menos 8 caracteres.')
            return redirect('registrar')
        
        # Crear usuario
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        
        # Asignar rol de recepcionista
        UsuarioRol.objects.create(usuario=user, rol='recepcionista')
        
        # Login automático del usuario
        login(request, user)
        
        # Refresca el usuario en la sesión para que Django reconozca el rol
        request.user = User.objects.get(pk=user.pk)
        
        messages.success(request, '✅ Registro exitoso. ¡Bienvenido a LogiCo!')
        return redirect('index2')  # Va directo a index2
    
    return render(request, 'registrar.html')
# =====================================================
# MENÚ Y REPORTES
# =====================================================

@login_required(login_url='login')
def reportes_menu(request):
    return render(request, 'reportes_menu.html')

@login_required(login_url='login')
def reportes_menu2(request):
    return render(request, 'reportes_menu2.html')

# =====================================================
# CRUD FARMACIA - SOLO ADMIN
# =====================================================

@login_required(login_url='login')
@user_passes_test(es_admin)
def farmacia_list(request):
    farmacias = Farmacia.objects.all()
    return render(request, 'farmacia_list.html', {'farmacias': farmacias})


@login_required(login_url='login')
@user_passes_test(es_admin)
def farmacia_create(request):
    if request.method == 'POST':
        form = FarmaciaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('farmacia_list')
    else:
        form = FarmaciaForm()
    return render(request, 'farmacia_form.html', {'form': form})


@login_required(login_url='login')
@user_passes_test(es_admin)
def farmacia_update(request, pk):
    farmacia = get_object_or_404(Farmacia, pk=pk)
    if request.method == 'POST':
        form = FarmaciaForm(request.POST, instance=farmacia)
        if form.is_valid():
            form.save()
            return redirect('farmacia_list')
    else:
        form = FarmaciaForm(instance=farmacia)
    return render(request, 'farmacia_form.html', {'form': form})


@login_required(login_url='login')
@user_passes_test(es_admin)
def farmacia_delete(request, pk):
    farmacia = get_object_or_404(Farmacia, pk=pk)
    if request.method == 'POST':
        farmacia.delete()
        return redirect('farmacia_list')
    return render(request, 'farmacia_delete.html', {'farmacia': farmacia})


# =====================================================
# CRUD MOTO - SOLO ADMIN
# =====================================================

@login_required(login_url='login')
@user_passes_test(es_admin)
def moto_list(request):
    motos = Moto.objects.all()
    return render(request, 'moto_list.html', {'motos': motos})


@login_required(login_url='login')
@user_passes_test(es_admin)
def moto_create(request):
    if request.method == 'POST':
        form = MotoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('moto_list')
    else:
        form = MotoForm()
    return render(request, 'moto_form.html', {'form': form})


@login_required(login_url='login')
@user_passes_test(es_admin)
def moto_update(request, pk):
    moto = get_object_or_404(Moto, pk=pk)
    if request.method == 'POST':
        form = MotoForm(request.POST, instance=moto)
        if form.is_valid():
            form.save()
            return redirect('moto_list')
    else:
        form = MotoForm(instance=moto)
    return render(request, 'moto_form.html', {'form': form})


@login_required(login_url='login')
@user_passes_test(es_admin)
def moto_delete(request, pk):
    moto = get_object_or_404(Moto, pk=pk)
    if request.method == 'POST':
        moto.delete()
        return redirect('moto_list')
    return render(request, 'moto_delete.html', {'moto': moto})


# =====================================================
# CRUD MOTORISTA - SOLO ADMIN
# =====================================================

@login_required(login_url='login')
@user_passes_test(es_admin)
def motorista_list(request):
    motoristas = Motorista.objects.all()
    return render(request, 'motorista_list.html', {'motoristas': motoristas})


@login_required(login_url='login')
@user_passes_test(es_admin)
def motorista_create(request):
    if request.method == 'POST':
        form = MotoristaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('motorista_list')
    else:
        form = MotoristaForm()
    return render(request, 'motorista_form.html', {'form': form})


@login_required(login_url='login')
@user_passes_test(es_admin)
def motorista_update(request, pk):
    motorista = get_object_or_404(Motorista, pk=pk)
    if request.method == 'POST':
        form = MotoristaForm(request.POST, instance=motorista)
        if form.is_valid():
            form.save()
            return redirect('motorista_list')
    else:
        form = MotoristaForm(instance=motorista)
    return render(request, 'motorista_form.html', {'form': form})


@login_required(login_url='login')
@user_passes_test(es_admin)
def motorista_delete(request, pk):
    motorista = get_object_or_404(Motorista, pk=pk)
    if request.method == 'POST':
        motorista.delete()
        return redirect('motorista_list')
    return render(request, 'motorista_delete.html', {'motorista': motorista})


# =====================================================
# CRUD ASIGNACIÓN MOTO - SOLO ADMIN
# =====================================================

@login_required(login_url='login')
@user_passes_test(es_admin)
def asignacion_moto_list(request):
    asignaciones = AsignacionMoto.objects.all()
    return render(request, 'asignacion_moto_list.html', {'asignaciones': asignaciones})


@login_required(login_url='login')
@user_passes_test(es_admin)
def asignacion_moto_create(request):
    if request.method == 'POST':
        form = AsignacionMotoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('asignacion_moto_list')
    else:
        form = AsignacionMotoForm()
    return render(request, 'asignacion_moto_form.html', {'form': form})


@login_required(login_url='login')
@user_passes_test(es_admin)
def asignacion_moto_update(request, pk):
    asignacion = get_object_or_404(AsignacionMoto, pk=pk)
    if request.method == 'POST':
        form = AsignacionMotoForm(request.POST, instance=asignacion)
        if form.is_valid():
            form.save()
            return redirect('asignacion_moto_list')
    else:
        form = AsignacionMotoForm(instance=asignacion)
    return render(request, 'asignacion_moto_form.html', {'form': form})


@login_required(login_url='login')
@user_passes_test(es_admin)
def asignacion_moto_delete(request, pk):
    asignacion = get_object_or_404(AsignacionMoto, pk=pk)
    if request.method == 'POST':
        asignacion.delete()
        return redirect('asignacion_moto_list')
    return render(request, 'asignacion_moto_delete.html', {'asignacion': asignacion})


# =====================================================
# CRUD ASIGNACIÓN FARMACIA - SOLO ADMIN
# =====================================================

@login_required(login_url='login')
@user_passes_test(es_admin)
def asignacion_farmacia_list(request):
    asignaciones = AsignacionFarmacia.objects.all()
    return render(request, 'asignacion_farmacia_list.html', {'asignaciones': asignaciones})


@login_required(login_url='login')
@user_passes_test(es_admin)
def asignacion_farmacia_create(request):
    if request.method == 'POST':
        form = AsignacionFarmaciaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('asignacion_farmacia_list')
    else:
        form = AsignacionFarmaciaForm()
    return render(request, 'asignacion_farmacia_form.html', {'form': form})


@login_required(login_url='login')
@user_passes_test(es_admin)
def asignacion_farmacia_update(request, pk):
    asignacion = get_object_or_404(AsignacionFarmacia, pk=pk)
    if request.method == 'POST':
        form = AsignacionFarmaciaForm(request.POST, instance=asignacion)
        if form.is_valid():
            form.save()
            return redirect('asignacion_farmacia_list')
    else:
        form = AsignacionFarmaciaForm(instance=asignacion)
    return render(request, 'asignacion_farmacia_form.html', {'form': form})


@login_required(login_url='login')
@user_passes_test(es_admin)
def asignacion_farmacia_delete(request, pk):
    asignacion = get_object_or_404(AsignacionFarmacia, pk=pk)
    if request.method == 'POST':
        asignacion.delete()
        return redirect('asignacion_farmacia_list')
    return render(request, 'asignacion_farmacia_delete.html', {'asignacion': asignacion})


# =====================================================
# CRUD MOVIMIENTO
# =====================================================

@login_required(login_url='login')
@user_passes_test(es_admin)
def movimiento_list(request):
    movimientos = Movimiento.objects.all()
    return render(request, 'movimiento_list.html', {'movimientos': movimientos})


@login_required(login_url='login')
@user_passes_test(es_recepcionista)
def movimiento_list2(request):
    """Solo recepcionista puede ver este listado"""
    movimientos = Movimiento.objects.all()
    return render(request, 'movimiento_list2.html', {'movimientos': movimientos})


@login_required(login_url='login')
@user_passes_test(es_admin)
def movimiento_create(request):
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movimiento_list')
    else:
        form = MovimientoForm()
    return render(request, 'movimiento_form.html', {'form': form})


@login_required(login_url='login')
@user_passes_test(es_recepcionista)
def movimiento_create2(request):
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movimiento_list2')
    else:
        form = MovimientoForm()
    return render(request, 'movimiento_form2.html', {'form': form})


@login_required(login_url='login')
@user_passes_test(es_admin)
def movimiento_update(request, pk):
    movimiento = get_object_or_404(Movimiento, pk=pk)
    if request.method == 'POST':
        form = MovimientoForm(request.POST, instance=movimiento)
        if form.is_valid():
            form.save()
            return redirect('movimiento_list')
    else:
        form = MovimientoForm(instance=movimiento)
    return render(request, 'movimiento_form.html', {'form': form})


@login_required(login_url='login')
@user_passes_test(es_admin)
def movimiento_delete(request, pk):
    movimiento = get_object_or_404(Movimiento, pk=pk)
    if request.method == 'POST':
        movimiento.delete()
        return redirect('movimiento_list')
    return render(request, 'movimiento_delete.html', {'movimiento': movimiento})


# =====================================================
# COMBOS DINÁMICOS
# =====================================================

def cargar_provincias(request):
    region = request.GET.get('region')
    provincias_por_region = {
        "Metropolitana de Santiago": ["Santiago", "Cordillera", "Chacabuco", "Maipo", "Melipilla", "Talagante"],
    }
    provincias = provincias_por_region.get(region, [])
    return JsonResponse({'provincias': provincias})


def cargar_comunas(request):
    provincia = request.GET.get('provincia')
    comunas_por_provincia = {
        "Santiago": ["Santiago", "Cerrillos", "Maipú", "La Florida"],
    }
    comunas = comunas_por_provincia.get(provincia, [])
    return JsonResponse({'comunas': comunas})


# =====================================================
# REPORTES
# =====================================================

@login_required(login_url='login')
def reporte_movimientos(request):
    tipo = request.GET.get("tipo")
    fecha = request.GET.get("fecha")
    mes = request.GET.get("mes")
    anio = request.GET.get("anio")

    movimientos = Movimiento.objects.all()

    if tipo == "DIARIO" and fecha:
        movimientos = movimientos.filter(fecha_registro__date=fecha)
    elif tipo == "MENSUAL" and mes and anio:
        movimientos = movimientos.filter(
            fecha_registro__year=anio,
            fecha_registro__month=mes
        )
    elif tipo == "ANUAL" and anio:
        movimientos = movimientos.filter(fecha_registro__year=anio)

    if tipo:
        ReporteMovimiento.objects.create(
            tipo=tipo,
            generado_por=request.user.username,
            total_movimientos=movimientos.count()
        )

    context = {
        "movimientos": movimientos,
        "tipo": tipo,
        "fecha": fecha,
        "mes": mes,
        "anio": anio,
    }

    return render(request, "reporte_resultado.html", context)


@login_required(login_url='login')
def descargar_reporte_pdf(request):
    tipo = request.GET.get("tipo")
    fecha = request.GET.get("fecha")
    mes = request.GET.get("mes")
    anio = request.GET.get("anio")

    movimientos = Movimiento.objects.all()

    if tipo == "DIARIO" and fecha:
        movimientos = movimientos.filter(fecha_registro__date=fecha)
    elif tipo == "MENSUAL" and mes and anio:
        movimientos = movimientos.filter(
            fecha_registro__year=anio,
            fecha_registro__month=mes
        )
    elif tipo == "ANUAL" and anio:
        movimientos = movimientos.filter(fecha_registro__year=anio)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=reporte_movimientos.pdf'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    y = height - 50

    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, f"Reporte de Movimientos - {tipo}")
    y -= 30

    p.setFont("Helvetica", 12)
    if tipo == "DIARIO":
        p.drawString(50, y, f"Fecha: {fecha}")
    elif tipo == "MENSUAL":
        p.drawString(50, y, f"Mes: {mes} / Año: {anio}")
    elif tipo == "ANUAL":
        p.drawString(50, y, f"Año: {anio}")
    y -= 30

    p.setFont("Helvetica-Bold", 10)
    p.drawString(40, y, "Código")
    p.drawString(100, y, "Tipo")
    p.drawString(160, y, "Estado")
    p.drawString(230, y, "Fecha")
    p.drawString(300, y, "Motorista")
    p.drawString(380, y, "Origen")
    p.drawString(470, y, "Destino")
    y -= 18

    p.setFont("Helvetica", 9)

    for m in movimientos:
        if y < 60:
            p.showPage()
            y = height - 50
            p.setFont("Helvetica-Bold", 10)
            p.drawString(40, y, "Código")
            p.drawString(100, y, "Tipo")
            p.drawString(160, y, "Estado")
            p.drawString(230, y, "Fecha")
            p.drawString(300, y, "Motorista")
            p.drawString(380, y, "Origen")
            p.drawString(470, y, "Destino")
            y -= 18
            p.setFont("Helvetica", 9)

        p.drawString(40, y, str(m.codigo))
        p.drawString(100, y, str(m.tipo))
        p.drawString(160, y, str(m.estado))
        p.drawString(230, y, m.fecha_registro.strftime("%Y-%m-%d"))
        p.drawString(300, y, m.motorista.nombre if m.motorista else "")
        p.drawString(380, y, m.farmacia_origen.nombre if m.farmacia_origen else "")
        p.drawString(470, y, m.destino if m.destino else "")

        y -= 15

    p.showPage()
    p.save()
    return response


def dashboard_usuario(request):
    return render(request, "dashboard_usuario.html")



@require_http_methods(["GET", "POST"])
def recuperar_password(request):
    """Enviar código de recuperación por email"""
    if request.method == "POST":
        email = request.POST.get('email', '').strip()
        
        try:
            user = User.objects.get(email=email)
            
            # Elimina código anterior si existe
            PasswordRecoveryCode.objects.filter(user=user).delete()
            
            # Crea nuevo código
            PasswordRecoveryCode.objects.create(user=user)
            
            messages.success(request, f"✔ Código enviado a {email}. Revisa tu bandeja de entrada.")
            return redirect('verificar_codigo')
        except User.DoesNotExist:
            messages.error(request, "❌ No existe cuenta con ese email.")
    
    return render(request, 'recuperar_password.html')


@require_http_methods(["GET", "POST"])
def verificar_codigo(request):
    """Verificar código de recuperación"""
    if request.method == "POST":
        email = request.POST.get('email', '').strip()
        codigo = request.POST.get('codigo', '').strip().upper()
        
        try:
            user = User.objects.get(email=email)
            recovery = PasswordRecoveryCode.objects.get(user=user)
            
            if not recovery.is_valid():
                messages.error(request, "❌ El código ha expirado. Solicita uno nuevo.")
                return redirect('recuperar_password')
            
            if recovery.code != codigo:
                messages.error(request, "❌ Código incorrecto.")
                return render(request, 'verificar_codigo.html', {'email': email})
            
            # Código válido, redirige a cambiar contraseña
            request.session['recovery_email'] = email
            request.session['codigo_verificado'] = True
            messages.success(request, "✔ Código verificado. Establece tu nueva contraseña.")
            return redirect('cambiar_password_recuperacion')
        
        except User.DoesNotExist:
            messages.error(request, "❌ Email no encontrado.")
        except PasswordRecoveryCode.DoesNotExist:
            messages.error(request, "❌ Solicita un código primero.")
    
    return render(request, 'verificar_codigo.html')


@require_http_methods(["GET", "POST"])
def cambiar_password_recuperacion(request):
    """Cambiar contraseña después de verificar código"""
    if not request.session.get('codigo_verificado'):
        messages.error(request, "❌ Debes verificar el código primero.")
        return redirect('recuperar_password')
    
    if request.method == "POST":
        email = request.session.get('recovery_email')
        password1 = request.POST.get('password1', '').strip()
        password2 = request.POST.get('password2', '').strip()
        
        if len(password1) < 8:
            messages.error(request, "❌ La contraseña debe tener al menos 8 caracteres.")
        elif password1 != password2:
            messages.error(request, "❌ Las contraseñas no coinciden.")
        else:
            try:
                user = User.objects.get(email=email)
                user.set_password(password1)
                user.save()
                
                # Marca código como usado
                recovery = PasswordRecoveryCode.objects.get(user=user)
                recovery.is_used = True
                recovery.save()
                
                # Limpia sesión
                del request.session['recovery_email']
                del request.session['codigo_verificado']
                
                messages.success(request, "✔ Contraseña actualizada correctamente. Inicia sesión.")
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, "❌ Error al actualizar contraseña.")
    
    return render(request, 'cambiar_password_recuperacion.html')


def employeeView(request):
   empleados = Employee.objects.all()
   data = {'employees': list(empleados.values('name'))}
   
   return JsonResponse(data)


@api_view(['GET', 'POST'])
def student_list(request):
    if request.method == 'GET':
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)