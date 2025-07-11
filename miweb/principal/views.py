from django.shortcuts import render, get_object_or_404 ,redirect
from .forms import RegistroForm
from .models import Registro, DEPARTAMENTO_CHOICES, COLONIAS_COMUNIDADES_CHOICES, CONCEPTOS_CHOICES, AVANCE_CHOICES
from datetime import datetime
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.timezone import now
from django.db.models import Count, Q
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.utils.dateparse import parse_date
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

def signin(request):
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username= username, password = password)

        if user is not None:
            login(request, user)
            return redirect('lista_registros')

        else: 
            return render(request, 'registro/login.html', {'error': 'Usuario o contraseña incorrecto'})
    
    else:
        
        return render(request, 'registro/login.html')


def logout_user(request):
    logout(request)
    messages.success(request, ("Has cerrado Sesión"))
    return redirect('inicio')


# Create your views here.
'''
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('lista_registros')  
        else:
            return render(request, 'registro/login.html', {'error': 'Usuario o contraseña incorrecto'})

    return render(request, 'registro/login.html')
'''



def inicio(request):
    fecha_actual = datetime.now().date()
    return render(request, 'registro/inicio.html')

#Esta Funicion de momento no sirve
@login_required
def fecha_actual_panel(request):
    fecha_actual = datetime.now().date()
    return render(request, 'registro/base.html', {'fecha_actual': fecha_actual})

def fecha_actual(request):
    return {
        'fecha_actual': now()
    }

@login_required
def inicio_sesion(request):
    return render(request, 'registro/formulario_inicio_sesion.html')


@login_required
def regristo_solicitudes(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.usuario= request.user
            registro.save()
            #form.save()
            return redirect('lista_registros')
    else:
        form= RegistroForm()
    return render(request, 'registro.html', {'form': form})


class RegistroCreateView(CreateView):
    model = Registro
    form_class = RegistroForm
    template_name = 'registro/registro_form.html'
    success_url = reverse_lazy('lista_registros')

    # 👇 Aquí agregas este método
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

@login_required
def lista_registros(request):
    
    registros = Registro.objects.all().order_by('numero_folio')


    # Filtros
    folio = request.GET.get('folio')
    departamento = request.GET.get('departamento')
    solicitante = request.GET.get('solicitante')
    colonia = request.GET.get('colonia')
    tipo_solicitud = request.GET.get('tipo_solicitud')
    avance = request.GET.get('avance')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    if folio:
        registros = registros.filter(numero_folio=folio)
    if departamento:
        registros = registros.filter(departamento_a_canalizar=departamento)
    if solicitante:
        registros = registros.filter(solicitante__icontains=solicitante)
    if colonia:
        registros = registros.filter(colonia_o_comunidad=colonia)
    if tipo_solicitud:
        registros = registros.filter(tipo_solicitud=tipo_solicitud)
    if avance:
        registros = registros.filter(avance=avance)

    # Filtro por rango de fechas
    if fecha_inicio and fecha_fin:
        registros = registros.filter(fecha_solicitud__range=[fecha_inicio, fecha_fin])
    elif fecha_inicio:
        registros = registros.filter(fecha_solicitud__gte=fecha_inicio)
    elif fecha_fin:
        registros = registros.filter(fecha_solicitud__lte=fecha_fin)

    # Paginación
    paginator = Paginator(registros, 10)
    page = request.GET.get('page')
    registros = paginator.get_page(page)
    nums = "a" * registros.paginator.num_pages

    return render(request, 'registro/lista.html', {
        'registros': registros,
        'nums': nums,
        'tipo_solicitud_choices': CONCEPTOS_CHOICES,
        'tipo_departamento_choices': DEPARTAMENTO_CHOICES,
        'tipo_colonia_choices': COLONIAS_COMUNIDADES_CHOICES,
        'tipo_avance_choices': AVANCE_CHOICES,
    })



@login_required
def editar_registro(request, pk):
    registro = get_object_or_404(Registro, pk=pk)
    if request.method == 'POST':
        form = RegistroForm(request.POST, instance=registro)
        if form.is_valid():
            form.save()
            return redirect('lista_registros')  
    else:
        form = RegistroForm(instance=registro)
    return render(request, 'registro/editar.html', {'form': form})


@login_required
def eliminar_registro(request, id):
    registro = get_object_or_404(Registro, pk=id)
    registro.delete()
    return redirect('lista_registros')

@login_required
def graficas_avance(request):
    estado_valores = {
        'proceso': 50,
        'atendido': 100,
        'cancelado': 0
    }

    dep_dict = dict(DEPARTAMENTO_CHOICES)

    departamentos = Registro.objects.values_list('departamento_a_canalizar', flat=True).distinct()

    etiquetas = []
    porcentajes = []
    datos_departamento = []

    total_global = 0
    total_atendidas = 0
    total_proceso = 0
    total_canceladas = 0
    suma_porcentajes = 0

    for depto in departamentos:
        registros = Registro.objects.filter(departamento_a_canalizar=depto)
        total = registros.count()
        if total == 0:
            continue

        atendidas = registros.filter(avance='atendido').count()
        proceso = registros.filter(avance='proceso').count()
        canceladas = registros.filter(avance='cancelado').count()

        suma_valores = sum(estado_valores.get(r.avance, 0) for r in registros)
        promedio = round(suma_valores / total, 2)

        nombre_legible = dep_dict.get(depto, depto)

        etiquetas.append(nombre_legible)
        porcentajes.append(promedio)

        datos_departamento.append({
            'departamento_a_canalizar': nombre_legible,
            'atendidas': atendidas,
            'proceso': proceso,
            'canceladas': canceladas,
            'total': total,
            'porcentaje_avance': promedio
        })

        # Acumulamos totales globales
        total_global += total
        total_atendidas += atendidas
        total_proceso += proceso
        total_canceladas += canceladas
        suma_porcentajes += suma_valores

    porcentaje_global = round(suma_porcentajes / total_global, 2) if total_global > 0 else 0

    context = {
        'etiquetas': etiquetas,
        'porcentajes': porcentajes,
        'datos_departamento': datos_departamento,
        'total_global': total_global,
        'total_atendidas': total_atendidas,
        'total_proceso': total_proceso,
        'total_canceladas': total_canceladas,
        'porcentaje_global': porcentaje_global,
    }

    return render(request, 'registro/graficas.html', context)


@login_required
def tabla_colonias(request):
    estado_valores = {
        'proceso': 50,
        'atendido': 100,
        'cancelado': 0
    }

    colonias = Registro.objects.values_list('colonia_o_comunidad', flat=True).distinct()

    datos_colonias = []
    etiquetas = []
    porcentajes = []

    total_general = 0
    total_atendidas = 0
    total_proceso = 0
    total_canceladas = 0
    suma_porcentajes = 0
    total_colonias_con_registros = 0

    diccionario_colonias = dict(COLONIAS_COMUNIDADES_CHOICES)

    for colonia in colonias:
        registros = Registro.objects.filter(colonia_o_comunidad=colonia)
        total = registros.count()
        if total == 0:
            continue

        atendidas = registros.filter(avance='atendido').count()
        proceso = registros.filter(avance='proceso').count()
        canceladas = registros.filter(avance='cancelado').count()

        suma_valores = sum(estado_valores.get(reg.avance, 0) for reg in registros)
        porcentaje = round(suma_valores / total, 2)

        nombre_legible = diccionario_colonias.get(colonia, colonia)

        datos_colonias.append({
            'colonia': nombre_legible,
            'atendidas': atendidas,
            'proceso': proceso,
            'canceladas': canceladas,
            'total': total,
            'porcentaje': porcentaje,
        })

        etiquetas.append(nombre_legible)
        porcentajes.append(porcentaje)

        # Totales generales
        total_general += total
        total_atendidas += atendidas
        total_proceso += proceso
        total_canceladas += canceladas
        suma_porcentajes += porcentaje
        total_colonias_con_registros += 1

    # Porcentaje promedio general
    porcentaje_general = round(suma_porcentajes / total_colonias_con_registros, 2) if total_colonias_con_registros else 0

    context = {
        'datos_colonias': datos_colonias,
        'etiquetas': etiquetas,
        'porcentajes': porcentajes,
        'total_general': total_general,
        'total_atendidas': total_atendidas,
        'total_proceso': total_proceso,
        'total_canceladas': total_canceladas,
        'porcentaje_general': porcentaje_general,
    }

    return render(request, 'registro/colonias.html', context)





#codigo en proceso &///////////////////////////////////////////////////////////////
@login_required
def tabla_conceptos(request):
    estado_valores = {
        'proceso': 50,
        'atendido': 100,
        'cancelado': 0
    }

    conceptos = Registro.objects.values_list('tipo_solicitud', flat=True).distinct()

    datos_conceptos = []
    etiquetas = []
    porcentajes = []

    diccionario_conceptos = dict(CONCEPTOS_CHOICES)

    # Totales globales
    total_global = 0
    total_atendidas = 0
    total_proceso = 0
    total_canceladas = 0
    suma_porcentajes = 0

    for concepto in conceptos:
        registros = Registro.objects.filter(tipo_solicitud=concepto)
        total = registros.count()
        if total == 0:
            continue

        atendidas = registros.filter(avance='atendido').count()
        proceso = registros.filter(avance='proceso').count()
        canceladas = registros.filter(avance='cancelado').count()

        suma_valores = sum(estado_valores.get(reg.avance, 0) for reg in registros)
        porcentaje = round(suma_valores / total, 2)

        nombre_legible = diccionario_conceptos.get(concepto, concepto)

        datos_conceptos.append({
            'concepto': nombre_legible,
            'atendidas': atendidas,
            'proceso': proceso,
            'canceladas': canceladas,
            'total': total,
            'porcentaje': porcentaje,
        })

        etiquetas.append(nombre_legible)
        porcentajes.append(porcentaje)

        # Acumular totales globales
        total_global += total
        total_atendidas += atendidas
        total_proceso += proceso
        total_canceladas += canceladas
        suma_porcentajes += suma_valores

    porcentaje_global = round(suma_porcentajes / total_global, 2) if total_global > 0 else 0

    context = {
        'datos_conceptos': datos_conceptos,
        'etiquetas': etiquetas,
        'porcentajes': porcentajes,
        'total_global': total_global,
        'total_atendidas': total_atendidas,
        'total_proceso': total_proceso,
        'total_canceladas': total_canceladas,
        'porcentaje_global': porcentaje_global,
    }

    return render(request, 'registro/conceptos.html', context)




@login_required
def exportar_pdf(request):
    registros = Registro.objects.all()

    # Aplica los filtros igual que en lista_registros
    folio = request.GET.get('folio')
    departamento = request.GET.get('departamento')
    solicitante = request.GET.get('solicitante')
    colonia = request.GET.get('colonia')
    tipo_solicitud = request.GET.get('tipo_solicitud')
    avance = request.GET.get('avance')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    

    if folio:
        registros = registros.filter(numero_folio=folio)
    if departamento:
        registros = registros.filter(departamento_a_canalizar=departamento)
    if solicitante:
        registros = registros.filter(solicitante__icontains=solicitante)
    if colonia:
        registros = registros.filter(colonia_o_comunidad=colonia)
    if tipo_solicitud:
        registros = registros.filter(tipo_solicitud=tipo_solicitud)
    
    if avance:
        registros = registros.filter(avance= avance)

    if fecha_inicio:
        registros = registros.filter(fecha_solicitud__gte=parse_date(fecha_inicio))
    
    if fecha_fin:
        registros = registros.filter(fecha_solicitud__lte=parse_date(fecha_fin))


    template = get_template('registro/pdf_tabla.html')
    context = {
        'registros': registros,
        'now': now(),  # << aquí usas la fecha y hora actual para el footer
    }
    html = template.render({'registros': registros})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="registros.pdf"'

  
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)
    return response


