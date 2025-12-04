from django.shortcuts import render, redirect, get_object_or_404
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import JsonResponse, HttpResponse
from .models import Farmacia, Moto, Motorista, Movimiento, AsignacionMoto, AsignacionFarmacia, ReporteMovimiento
from .forms import (
    FarmaciaForm,
    MotoForm,
    MotoristaForm,
    MovimientoForm,
    AsignacionMotoForm,
    AsignacionFarmaciaForm
)


# =====================================================
# PÁGINA PRINCIPAL
# =====================================================
def index(request):
    return render(request, 'index.html')

def reportes_menu(request):
    return render(request, 'reportes_menu.html')


# =====================================================
# CRUD FARMACIA
# =====================================================
def farmacia_list(request):
    farmacias = Farmacia.objects.all()
    return render(request, 'farmacia_list.html', {'farmacias': farmacias})

def farmacia_create(request):
    if request.method == 'POST':
        form = FarmaciaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('farmacia_list')
    else:
        form = FarmaciaForm()
    return render(request, 'farmacia_form.html', {'form': form})

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

def farmacia_delete(request, pk):
    farmacia = get_object_or_404(Farmacia, pk=pk)
    if request.method == 'POST':
        farmacia.delete()
        return redirect('farmacia_list')
    return render(request, 'farmacia_delete.html', {'farmacia': farmacia})



def moto_list(request):
    motos = Moto.objects.all()
    return render(request, 'moto_list.html', {'motos': motos})

def moto_create(request):
    if request.method == 'POST':
        form = MotoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('moto_list')
    else:
        form = MotoForm()
    return render(request, 'moto_form.html', {'form': form})

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

def moto_delete(request, pk):
    moto = get_object_or_404(Moto, pk=pk)
    if request.method == 'POST':
        moto.delete()
        return redirect('moto_list')
    return render(request, 'moto_delete.html', {'moto': moto})


# =====================================================
# CRUD MOTORISTA
# =====================================================
def motorista_list(request):
    motoristas = Motorista.objects.all()
    return render(request, 'motorista_list.html', {'motoristas': motoristas})

def motorista_create(request):
    if request.method == 'POST':
        form = MotoristaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('motorista_list')
    else:
        form = MotoristaForm()
    return render(request, 'motorista_form.html', {'form': form})

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

def motorista_delete(request, pk):
    motorista = get_object_or_404(Motorista, pk=pk)
    if request.method == 'POST':
        motorista.delete()
        return redirect('motorista_list')
    return render(request, 'motorista_delete.html', {'motorista': motorista})


# =====================================================
# CRUD ASIGNACIÓN MOTO
# =====================================================
def asignacion_moto_list(request):
    asignaciones = AsignacionMoto.objects.all()
    return render(request, 'asignacion_moto_list.html', {'asignaciones': asignaciones})

def asignacion_moto_create(request):
    if request.method == 'POST':
        form = AsignacionMotoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('asignacion_moto_list')
    else:
        form = AsignacionMotoForm()
    return render(request, 'asignacion_moto_form.html', {'form': form})

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

def asignacion_moto_delete(request, pk):
    asignacion = get_object_or_404(AsignacionMoto, pk=pk)
    if request.method == 'POST':
        asignacion.delete()
        return redirect('asignacion_moto_list')
    return render(request, 'asignacion_moto_delete.html', {'asignacion': asignacion})


# =====================================================
# CRUD ASIGNACIÓN FARMACIA
# =====================================================
def asignacion_farmacia_list(request):
    asignaciones = AsignacionFarmacia.objects.all()
    return render(request, 'asignacion_farmacia_list.html', {'asignaciones': asignaciones})

def asignacion_farmacia_create(request):
    if request.method == 'POST':
        form = AsignacionFarmaciaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('asignacion_farmacia_list')
    else:
        form = AsignacionFarmaciaForm()
    return render(request, 'asignacion_farmacia_form.html', {'form': form})

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

def asignacion_farmacia_delete(request, pk):
    asignacion = get_object_or_404(AsignacionFarmacia, pk=pk)
    if request.method == 'POST':
        asignacion.delete()
        return redirect('asignacion_farmacia_list')
    return render(request, 'asignacion_farmacia_delete.html', {'asignacion': asignacion})


# =====================================================
# CRUD MOVIMIENTO
# =====================================================
def movimiento_list(request):
    movimientos = Movimiento.objects.all()
    return render(request, 'movimiento_list.html', {'movimientos': movimientos})

def movimiento_create(request):
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movimiento_list')
    else:
        form = MovimientoForm()
    return render(request, 'movimiento_form.html', {'form': form})

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

def movimiento_delete(request, pk):
    movimiento = get_object_or_404(Movimiento, pk=pk)
    if request.method == 'POST':
        movimiento.delete()
        return redirect('movimiento_list')
    return render(request, 'movimiento_delete.html', {'movimiento': movimiento})

def cargar_provincias(request):
    region = request.GET.get('region')
    provincias_por_region = {
        "Arica y Parinacota": ["Arica", "Parinacota"],
        "Tarapacá": ["Iquique", "Tamarugal"],
        "Antofagasta": ["Antofagasta", "El Loa", "Tocopilla"],
        "Atacama": ["Copiapó", "Chañaral", "Huasco"],
        "Coquimbo": ["Elqui", "Choapa", "Limarí"],
        "Valparaíso": ["Valparaíso", "Quillota", "San Antonio", "Petorca", "Marga Marga", "Los Andes", "San Felipe de Aconcagua", "Isla de Pascua"],
        "Metropolitana de Santiago": ["Santiago", "Cordillera", "Chacabuco", "Maipo", "Melipilla", "Talagante"],
        "Libertador General Bernardo O'Higgins": ["Cachapoal", "Colchagua", "Cardenal Caro"],
        "Maule": ["Talca", "Curicó", "Linares", "Cauquenes"],
        "Ñuble": ["Diguillín", "Itata", "Punilla"],
        "Biobío": ["Concepción", "Biobío", "Arauco"],
        "La Araucanía": ["Cautín", "Malleco"],
        "Los Ríos": ["Valdivia", "Ranco"],
        "Los Lagos": ["Llanquihue", "Osorno", "Chiloé", "Palena"],
        "Aysén del General Carlos Ibáñez del Campo": ["Coyhaique", "Aysén", "General Carrera", "Capitán Prat"],
        "Magallanes y la Antártica Chilena": ["Magallanes", "Última Esperanza", "Tierra del Fuego", "Antártica Chilena"],
    }

    provincias = provincias_por_region.get(region, [])
    return JsonResponse({'provincias': provincias})


def cargar_comunas(request):
    provincia = request.GET.get('provincia')

    comunas_por_provincia = {
        # ==== Región Metropolitana ====
        "Santiago": ["Santiago","Cerrillos","Cerro Navia","Conchalí","El Bosque","Estación Central","Huechuraba","Independencia","La Cisterna","La Florida","La Granja","La Pintana","La Reina","Las Condes","Lo Barnechea","Lo Espejo","Lo Prado","Macul","Maipú","Ñuñoa","Pedro Aguirre Cerda","Peñalolén","Providencia","Pudahuel","Quilicura","Quinta Normal","Recoleta","Renca","San Joaquín","San Miguel","San Ramón","Vitacura"],
        "Chacabuco": ["Colina","Lampa","Tiltil"],
        "Cordillera": ["Pirque","Puente Alto","San José de Maipo"],
        "Maipo": ["Buín","Calera de Tango","Paine","San Bernardo"],
        "Melipilla": ["Alhué","Curacaví","María Pinto","Melipilla","San Pedro"],
        "Talagante": ["El Monte","Isla de Maipo","Padre Hurtado","Peñaflor","Talagante"],

        # ==== Valparaíso ====
        "Valparaíso": ["Valparaíso","Viña del Mar","Concón","Puchuncaví","Quintero","Casablanca","Juan Fernández"],
        "San Antonio": ["San Antonio","Algarrobo","Cartagena","El Quisco","El Tabo","Santo Domingo"],
        "Marga Marga": ["Quilpué","Villa Alemana","Limache","Olmué"],
        "Petorca": ["La Ligua","Cabildo","Papudo","Petorca","Zapallar"],
        "Los Andes": ["Los Andes","Calle Larga","Rinconada","San Esteban"],
        "San Felipe de Aconcagua": ["San Felipe","Catemu","Llay-Llay","Panquehue","Putaendo","Santa María"],
        "Quillota": ["Quillota","Hijuelas","La Calera","La Cruz","Nogales"],
        "Isla de Pascua": ["Rapa Nui"],

        # ==== O’Higgins ====
        "Cachapoal": ["Rancagua","Codegua","Coinco","Coltauco","Doñihue","Graneros","Las Cabras","Machalí","Malloa","Mostazal","Olivar","Peumo","Pichidegua","Quinta de Tilcoco","Rengo","Requínoa","San Vicente de Tagua Tagua"],
        "Colchagua": ["San Fernando","Chépica","Chimbarongo","Lolol","Nancagua","Palmilla","Peralillo","Placilla","Pumanque","Santa Cruz"],
        "Cardenal Caro": ["Pichilemu","La Estrella","Litueche","Marchigüe","Navidad","Paredones"],

        # ==== Maule ====
        "Talca": ["Talca","Constitución","Curepto","Empedrado","Maule","Pelarco","Pencahue","Río Claro","San Clemente","San Rafael"],
        "Curicó": ["Curicó","Hualañé","Licantén","Molina","Rauco","Romeral","Sagrada Familia","Teno","Vichuquén"],
        "Linares": ["Linares","Colbún","Longaví","Parral","Retiro","San Javier","Villa Alegre","Yerbas Buenas"],
        "Cauquenes": ["Cauquenes","Chanco","Pelluhue"],

        # ==== Ñuble ====
        "Diguillín": ["Bulnes","Chillán","Chillán Viejo","El Carmen","Pemuco","Pinto","Quillón","San Ignacio","Yungay"],
        "Itata": ["Cobquecura","Coelemu","Ninhue","Portezuelo","Quirihue","Ránquil","Treguaco"],
        "Punilla": ["Coihueco","Ñiquén","San Carlos","San Fabián","San Nicolás"],

        # ==== Biobío ====
        "Concepción": ["Concepción","Coronel","Chiguayante","Florida","Hualpén","Hualqui","Lota","Penco","San Pedro de la Paz","Santa Juana","Talcahuano","Tomé"],
        "Arauco": ["Lebu","Arauco","Cañete","Contulmo","Curanilahue","Los Álamos","Tirúa"],
        "Biobío": ["Los Ángeles","Antuco","Cabrero","Laja","Mulchén","Nacimiento","Negrete","Quilaco","Quilleco","San Rosendo","Santa Bárbara","Tucapel","Yumbel","Alto Biobío"],

        # ==== Araucanía ====
        "Cautín": ["Temuco","Carahue","Cholchol","Cunco","Curarrehue","Freire","Galvarino","Gorbea","Lautaro","Loncoche","Melipeuco","Nueva Imperial","Padre Las Casas","Perquenco","Pitrufquén","Pucón","Puerto Saavedra","Teodoro Schmidt","Toltén","Vilcún","Villarrica"],
        "Malleco": ["Angol","Collipulli","Curacautín","Ercilla","Lonquimay","Los Sauces","Lumaco","Purén","Renaico","Traiguén","Victoria"],

        # ==== Los Ríos ====
        "Valdivia": ["Valdivia","Corral","Lanco","Los Lagos","Máfil","Mariquina","Paillaco","Panguipulli"],
        "Ranco": ["La Unión","Futrono","Lago Ranco","Río Bueno"],

        # ==== Los Lagos ====
        "Llanquihue": ["Puerto Montt","Puerto Varas","Frutillar","Llanquihue","Maullín","Los Muermos","Calbuco","Cochamó","Fresia"],
        "Chiloé": ["Castro","Ancud","Chonchi","Curaco de Vélez","Dalcahue","Puqueldón","Queilén","Quellón","Quemchi","Quinchao"],
        "Osorno": ["Osorno","Puerto Octay","Purranque","Puyehue","Río Negro","San Juan de la Costa","San Pablo"],
        "Palena": ["Chaitén","Futaleufú","Hualaihué","Palena"],

        # ==== Aysén ====
        "Coyhaique": ["Coyhaique","Lago Verde"],
        "Aysén": ["Aysén","Cisnes","Guaitecas"],
        "Capitán Prat": ["Cochrane","O'Higgins","Tortel"],
        "General Carrera": ["Chile Chico","Río Ibáñez"],

        # ==== Magallanes ====
        "Magallanes": ["Punta Arenas","Río Verde","San Gregorio","Laguna Blanca"],
        "Tierra del Fuego": ["Porvenir","Primavera","Timaukel"],
        "Última Esperanza": ["Natales","Torres del Paine"],
        "Antártica Chilena": ["Antártica","Cabo de Hornos"],

        # ==== Norte de Chile ====
        "Arica": ["Arica","Camarones"],
        "Parinacota": ["Putre","General Lagos"],
        "Iquique": ["Iquique","Alto Hospicio"],
        "Tamarugal": ["Pozo Almonte","Camiña","Colchane","Huara","Pica"],
        "Antofagasta": ["Antofagasta","Mejillones","Sierra Gorda","Taltal"],
        "El Loa": ["Calama","Ollagüe","San Pedro de Atacama"],
        "Tocopilla": ["Tocopilla","María Elena"],
        "Copiapó": ["Copiapó","Caldera","Tierra Amarilla"],
        "Chañaral": ["Chañaral","Diego de Almagro"],
        "Huasco": ["Vallenar","Alto del Carmen","Freirina","Huasco"],
        "Elqui": ["La Serena","Coquimbo","Andacollo","La Higuera","Paihuano","Vicuña"],
        "Limarí": ["Ovalle","Monte Patria","Combarbalá","Punitaqui","Río Hurtado"],
        "Choapa": ["Illapel","Canela","Los Vilos","Salamanca"]
    }

    comunas = comunas_por_provincia.get(provincia, [])
    return JsonResponse({'comunas': comunas})


def reporte_movimientos(request):
    tipo = request.GET.get("tipo")
    fecha = request.GET.get("fecha")
    mes = request.GET.get("mes")
    anio = request.GET.get("anio")

    movimientos = Movimiento.objects.all()

    if tipo == "DIARIO" and fecha:
        movimientos = movimientos.filter(
            fecha_registro__date=fecha
        )

    elif tipo == "MENSUAL" and mes and anio:
        movimientos = movimientos.filter(
            fecha_registro__year=anio,
            fecha_registro__month=mes
        )

    elif tipo == "ANUAL" and anio:
        movimientos = movimientos.filter(
            fecha_registro__year=anio
        )

    # Registrar automáticamente en ReporteMovimiento
    if tipo:
        ReporteMovimiento.objects.create(
            tipo=tipo,
            generado_por="Administrador del Sistema",
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

def descargar_reporte_pdf(request):
    tipo = request.GET.get("tipo")
    fecha = request.GET.get("fecha")
    mes = request.GET.get("mes")
    anio = request.GET.get("anio")

    movimientos = Movimiento.objects.all()

    if tipo == "DIARIO" and fecha:
        movimientos = movimientos.filter(
            fecha_registro__date=fecha
        )

    elif tipo == "MENSUAL" and mes and anio:
        movimientos = movimientos.filter(
            fecha_registro__year=anio,
            fecha_registro__month=mes
        )

    elif tipo == "ANUAL" and anio:
        movimientos = movimientos.filter(
            fecha_registro__year=anio
        )

    # ========================
    # GENERAR PDF
    # ========================

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=reporte_movimientos.pdf'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    y = height - 50

    # Título
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, f"Reporte de Movimientos - {tipo}")
    y -= 30

    # Filtros aplicados
    p.setFont("Helvetica", 12)
    if tipo == "DIARIO":
        p.drawString(50, y, f"Fecha: {fecha}")
    elif tipo == "MENSUAL":
        p.drawString(50, y, f"Mes: {mes} / Año: {anio}")
    elif tipo == "ANUAL":
        p.drawString(50, y, f"Año: {anio}")
    y -= 30

    # Encabezados de tabla
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
        if y < 60:  # Nueva página si se llena
            p.showPage()
            y = height - 50

            # Encabezados en nueva página
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

        # Datos del movimiento
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