from django.contrib import admin
from django.urls import path
from principal.views import inicio, inicio_sesion, signin, fecha_actual_panel
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('signin/', signin, name='login'),
    path('logout_user/', views.logout_user, name = 'logout'),
    path('', inicio, name='inicio'),
    path('inicio_sesion', inicio_sesion, name= 'sesion_empleado'),
    path('registro/', views.regristo_solicitudes, name= 'registro'),
    path('editar/<int:pk>', views.editar_registro, name='editar_registro'),
    path('eliminar/<int:id>/', views.eliminar_registro, name='eliminar_registro'),  
    path('lista/', views.lista_registros, name= 'lista_registros'),
    path('graficas/', views.graficas_avance, name='graficas_avance'),
    path('tabla-colonias/', views.tabla_colonias, name='tabla_colonias'),
    path('tabla-conceptos/', views.tabla_conceptos, name= 'tabla_conceptos'),
    path('exportar-pdf/', views.exportar_pdf, name='exportar_pdf'),

]

