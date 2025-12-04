from django.contrib import admin
from django.urls import path
from App import views


urlpatterns = [
    # ========== PÁGINA INICIAL ==========
    
    path('',views.paginaPrincipal, name='paginaPrincipal'),
    path('login/', views.login_view, name='login'),
    
    # urls.py
    path('logout/', views.logout_view, name='logout'),  
    path('cambiar-password/', views.cambiar_password, name='cambiar_password'),
    path('recuperar-password/', views.recuperar_password, name='recuperar_password'),
    
    path('index', views.index, name='index'),

    # ========== FARMACIA ==========
    path('farmacias/', views.farmacia_list, name='farmacia_list'),
    path('farmacias/crear/', views.farmacia_create, name='farmacia_create'),
    path('farmacias/editar/<int:pk>/', views.farmacia_update, name='farmacia_update'),
    path('farmacias/eliminar/<int:pk>/', views.farmacia_delete, name='farmacia_delete'),

    # ========== MOTO ==========
    path('motos/', views.moto_list, name='moto_list'),
    path('motos/crear/', views.moto_create, name='moto_create'),
    path('motos/editar/<int:pk>/', views.moto_update, name='moto_update'),
    path('motos/eliminar/<int:pk>/', views.moto_delete, name='moto_delete'),

    # ========== MOTORISTA ==========
    path('motoristas/', views.motorista_list, name='motorista_list'),
    path('motoristas/crear/', views.motorista_create, name='motorista_create'),
    path('motoristas/editar/<int:pk>/', views.motorista_update, name='motorista_update'),
    path('motoristas/eliminar/<int:pk>/', views.motorista_delete, name='motorista_delete'),

    # ========== ASIGNACIONES ==========
    path('asignacion-moto/', views.asignacion_moto_list, name='asignacion_moto_list'),
    path('asignacion-moto/crear/', views.asignacion_moto_create, name='asignacion_moto_create'),
    path('asignacion-moto/editar/<int:pk>/', views.asignacion_moto_update, name='asignacion_moto_update'),
    path('asignacion-moto/eliminar/<int:pk>/', views.asignacion_moto_delete, name='asignacion_moto_delete'),

    path('asignacion-farmacia/', views.asignacion_farmacia_list, name='asignacion_farmacia_list'),
    path('asignacion-farmacia/crear/', views.asignacion_farmacia_create, name='asignacion_farmacia_create'),
    path('asignacion-farmacia/editar/<int:pk>/', views.asignacion_farmacia_update, name='asignacion_farmacia_update'),
    path('asignacion-farmacia/eliminar/<int:pk>/', views.asignacion_farmacia_delete, name='asignacion_farmacia_delete'),

    # ========== MOVIMIENTOS ==========
    path('movimientos/', views.movimiento_list, name='movimiento_list'),
    path('movimientos/crear/', views.movimiento_create, name='movimiento_create'),
    path('movimientos/editar/<int:pk>/', views.movimiento_update, name='movimiento_update'),
    path('movimientos/eliminar/<int:pk>/', views.movimiento_delete, name='movimiento_delete'),

    # ========== AJAX: PROVINCIAS Y COMUNAS ==========
    path('ajax/cargar-provincias/', views.cargar_provincias, name='cargar_provincias'),
    path('ajax/cargar-comunas/', views.cargar_comunas, name='cargar_comunas'),

    
    path('reportes/', views.reportes_menu, name='reportes_menu'),
    path('reportes/resultados/', views.reporte_movimientos, name='reporte_movimientos'),
    path('reportes/descargar/pdf/', views.descargar_reporte_pdf, name='descargar_reporte_pdf'),

]

