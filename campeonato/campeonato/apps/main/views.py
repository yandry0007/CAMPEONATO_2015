# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.views.generic import FormView
from django.core.urlresolvers import reverse_lazy
from django.template import RequestContext
from django.core.mail import EmailMessage
from models import *
from forms import *

def lista_equipos_view(request):
	#Revisar consultas a la base de datos en la doc oficcioal de django 
	#Revisar consultas de SQL primas en django para escribir codigo sql
	equipos = Equipo.objects.all()
	ctx = {'equipos':equipos}
	return render_to_response('equipos.html', ctx, context_instance=RequestContext(request))

def index_view(request):	
    #equipos = equipo.objects.values('desequipo','puntos','gf','gc').order_by('-puntos','-gf','gc')
    torneos = Campeonato.objects.filter(estado=True)
    equipos = Equipo.objects.filter(fk_campeonato__estado__exact=True).order_by('-puntos','-gf','gc')
    return render_to_response('tabla_posciciones.html', context_instance=RequestContext(request,{'equipos':equipos, 'torneos':torneos}))


def ingresar_view(request):
	if not request.user.is_anonymous():
		return HttpResponseRedirect('/')
	if request.method == 'POST':
		formulario = AuthenticationForm(request.POST)
		if formulario.is_valid:
			usuario = request.POST['username']
			pwd = request.POST['password']
			acceso = authenticate(username=usuario, password=pwd)
			if acceso is not None:
				if acceso.is_active:
					login(request, acceso)
					return HttpResponseRedirect('/')
				else:
					#return render_to_response('noactivo.html', context_instance=RequestContext(request))
					return render_to_response('noactivo.html', {'error':True, 'formulario':formulario}, context_instance=RequestContext(request))
			else:
				#return render_to_response('nousuario.html', context_instance=RequestContext(request))
				return render_to_response('nousuario.html', {'error':True, 'formulario':formulario}, context_instance=RequestContext(request))
	else:
		formulario = AuthenticationForm()
	return render_to_response('ingresar.html',{'formulario':formulario}, context_instance=RequestContext(request))

def resultados_view(request,pagina):
	torneos = Campeonato.objects.filter(estado=True)
	#resultados = Encuentro.objects.filter(fk_local__fk_campeonato__estado__exact=True).order_by('fk_fecha')
  	resultados = Encuentro.objects.filter(jugado__exact=True).order_by('fk_fecha')

	#PAGINACION
	paginator = Paginator(resultados,6)
	try:
		page = int(pagina)
	except:
		page = 1
	try:
		resultados = paginator.page(page)
	except (EmptyPage, InvalidPage):
		resultados = paginator.page(paginator.num_pages)

	ctx = {'resultados':resultados, 'torneos':torneos}
	return render_to_response('resultados.html', ctx, context_instance=RequestContext(request))

def goleadores_view(request):
	jugadores = Goles.objects.exclude(goles=0).order_by('-goles','fk_user').filter(fk_user__fk_equipo__fk_campeonato__estado__exact=True)
	torneos = Campeonato.objects.filter(estado=True)
	return render_to_response('goleadores.html', context_instance=RequestContext(request,{'jugadores':jugadores, 'torneos': torneos}))

def print_goleadores_view(request):
	jugadores = Goles.objects.exclude(goles=0).order_by('-goles','fk_user').filter(fk_user__fk_equipo__fk_campeonato__estado__exact=True)
	torneos = Campeonato.objects.filter(estado=True)
	return render_to_response('print_goleadores.html', context_instance=RequestContext(request,{'jugadores':jugadores, 'torneos': torneos}))

def amonestados_view(request):
	#b = juego.objects.exclude(id=0)
	#tarjetas = b.juegotarjeta_set.all()
	torneos = Campeonato.objects.filter(estado=True)
	tarjetas = JuegoTarjeta.objects.filter(fk_jugador__fk_equipo__fk_campeonato__estado__exact=True).order_by('-fk_juego')
	return render_to_response('amonestados.html', context_instance=RequestContext(request,{'tarjetas':tarjetas, 'torneos':torneos}))

def contactenos_view(request):
	torneos = Campeonato.objects.filter(estado=True)
	info = "inicializando"
	if request.method=='POST':
		formulario = ContactoForm(request.POST)
		if formulario.is_valid():
			titulo = 'Mesaje del Campeonato CIS-UNL_2015'
			contenido = formulario.cleaned_data['mensaje']+"\n"
			contenido += 'Comunicarse a: ' + formulario.cleaned_data['correo']
			correo = EmailMessage(titulo, contenido, to=['yrramirezs@unl.edu.ec'])
			info = "Correo Enviado ok!!"
			try:
				correo.send()
			except Exception, e:
				return render_to_response('contactenos.html',{'info':info,'torneos':torneos}, context_instance=RequestContext(request))
	else:
		formulario = ContactoForm()
	return render_to_response('contactenos.html',{'info':info, 'formulario':formulario, 'torneos':torneos}, context_instance=RequestContext(request))

def salir_view(request):
	logout(request)
	return HttpResponseRedirect('/ingresar')

def jugadores_view(request,pagina):
	jugadores = Perfiles.objects.filter(fk_equipo__fk_campeonato__estado__exact=True)
	torneos = Campeonato.objects.filter(estado=True)
	equipos = Equipo.objects.filter(fk_campeonato__estado__exact=True)
	try:
		perfil = Perfiles.objects.get(fk_equipo__inscripcion=True)
	except:
		perfil = None


	#BUSCAR JUGADORES
	
	if request.method == "POST":
		pro = Perfiles.objects.filter(cedula__icontains = request.POST['texto'] )
		#PAGINACION
		paginator = Paginator(pro,7)
		try:
			page = int(pagina)
		except:
			page = 1
		try:
			pro = paginator.page(page)
		except (EmptyPage, InvalidPage):
			pro = paginator.page(paginator.num_pages)

		return render_to_response('jugadores.html',{'torneos':torneos,'pro':pro }, context_instance=RequestContext(request))

	#PAGINACION
	paginator = Paginator(jugadores,6)
	try:
		page = int(pagina)
	except:
		page = 1
	try:
		jugadores = paginator.page(page)
	except (EmptyPage, InvalidPage):
		jugadores = paginator.page(paginator.num_pages)

	ctx = {'jugadores':jugadores, 'torneos': torneos, 'equipos':equipos, 'perfil':perfil}
	return render_to_response('jugadores.html', ctx, context_instance=RequestContext(request))

def calendario_varones_view(request,pagina):
  torneos = Campeonato.objects.filter(estado=True)
  #encuentros = Encuentro.objects.filter(fk_local__fk_campeonato__estado__exact=True).order_by('fk_fecha')
  encuentros = Encuentro.objects.filter(jugado__exact=False, varones=True).order_by('fk_fecha')
  #PAGINACION
  paginator = Paginator(encuentros,4)
  try:
    page = int(pagina)
  except:
      page = 1
  try:
    encuentros = paginator.page(page)
  except (EmptyPage, InvalidPage):
    encuentros = paginator.page(paginator.num_pages)
  ctx = {'encuentros':encuentros, 'torneos': torneos}
  return render_to_response('calendario.html', ctx, context_instance=RequestContext(request))


def calendario_mujeres_view(request,pagina):
  torneos = Campeonato.objects.filter(estado=True)
  #encuentros = Encuentro.objects.filter(fk_local__fk_campeonato__estado__exact=True).order_by('fk_fecha')
  encuentros = Encuentro.objects.filter(jugado__exact=False, mujeres=True).order_by('fk_fecha')
  #PAGINACION
  paginator = Paginator(encuentros,4)
  try:
    page = int(pagina)
  except:
      page = 1
  try:
    encuentros = paginator.page(page)
  except (EmptyPage, InvalidPage):
    encuentros = paginator.page(paginator.num_pages)
  ctx = {'encuentros':encuentros, 'torneos': torneos}
  return render_to_response('calendario_mujeres.html', ctx, context_instance=RequestContext(request))

#@login_required(login_url='/ingresar')
def registrar_view(request):
	torneos = Campeonato.objects.filter(estado=True)
	info = "inicializando"
	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			form.save()
			info = "Registrado Satisfactoriamente!!"
			ctx = {'info':info,'torneos':torneos}
			return render_to_response('agregar_jugador.html',ctx, context_instance=RequestContext(request))
	else:
		form = LoginForm()
	ctx = {'form':form,'info':info,'torneos':torneos}
	return render_to_response('agregar_jugador.html',ctx, context_instance=RequestContext(request))


def single_jugador_view(request,id_jugador):
	torneos = Campeonato.objects.filter(estado=True)
	perfil = Perfiles.objects.get(id=id_jugador)
	ctx = {'perfil':perfil, 'torneos':torneos}
	return render_to_response('single_jugador.html',ctx, context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def agregar_perfil_view(request):
	torneos = Campeonato.objects.filter(estado=True)
	info = "iniciar"
	if request.method == "POST":
		form = PerfilForm(request.POST,request.FILES)
		if form.is_valid():
			form.save()
			info = "Agregado Satisfactoriamente!!!"
			ctx = {'info':info, 'torneos':torneos}
			return render_to_response('agregar_perfil.html',ctx, context_instance=RequestContext(request))
	else:
		form = PerfilForm()
	ctx = {'form':form,'info':info, 'torneos':torneos}
	return render_to_response('agregar_perfil.html',ctx, context_instance=RequestContext(request))

# class agregarPerfil(FormView):
# 	template_name = 'agregar_perfil.html'
# 	form_class = UserForm
# 	success_url = reverse_lazy('vista_agregar_perfil')
# 	def form_valid(self, form):
# 		user = form.save()
# 		fk_equipo = form.save()
# 		perfil = Perfiles()
# 		perfil.user = user
# 		perfil.nombres = form.cleaned_data['nombres']
# 		perfil.apellidos = form.cleaned_data['apellidos']
# 		perfil.cedula = form.cleaned_data['cedula']
# 		perfil.representante = form.cleaned_data['representante']
# 		perfil.capitan = form.cleaned_data['capitan']
# 		perfil.foto = form.cleaned_data['foto']
# 		perfil.estatura = form.cleaned_data['estatura']
# 		perfil.correo = form.cleaned_data['correo']
# 		perfil.telefono = form.cleaned_data['telefono']
# 		perfil.fk_equipo = fk_equipo
# 		perfil.save()
# 		return super(agregarPerfil , self).form_valid(form)


# class Registrarse(FormView):
# 	template_name = 'RegistrarUsuario.html' #envio una variable a registrarse y tengo q recogerla ahi
# 	form_class = UserForm
# 	success_url = reverse_lazy('registrarsee')

# 	def form_valid(self, form):
# 		user = form.save()
# 		perfil = Perfiles()
# 		perfil.user = user
# 		perfil.telefono = form.cleaned_data['telefono']
# 		perfil.photo = form.cleaned_data['photo']
# 		perfil.save()
# 		return super(Registrarse , self).form_valid(form)


def equipos_view(request,pagina):
	jugadores = Perfiles.objects.filter(fk_equipo__fk_campeonato__estado__exact=True)
	torneos = Campeonato.objects.filter(estado=True)
	equipos = Equipo.objects.filter(fk_campeonato__estado__exact=True)

	#PAGINACION
	paginator = Paginator(jugadores,5)
	try:
		page = int(pagina)
	except:
		page = 1
	try:
		jugadores = paginator.page(page)
	except (EmptyPage, InvalidPage):
		jugadores = paginator.page(paginator.num_pages)

	ctx = {'jugadores':jugadores, 'torneos': torneos, 'equipos':equipos}
	return render_to_response('equipos.html', ctx, context_instance=RequestContext(request))

def print_plantilla_view(request):
	torneos = Campeonato.objects.filter(estado=True)
	if request.method == "POST":
		plantilla = Perfiles.objects.filter(fk_equipo__nombre__icontains = request.POST['equipo'] )
		ctx = {'plantilla':plantilla, 'torneos':torneos}
		return render_to_response('print_plantilla.html', ctx, context_instance=RequestContext(request))
	return render_to_response('print_plantilla.html', {'torneos':torneos}, context_instance=RequestContext(request))

def print_encuentro_varones_view(request, id_encuentro):
	torneos = Campeonato.objects.filter(estado=True)
	planilla = Encuentro.objects.get(id=id_encuentro)
	j_local	= Perfiles.objects.filter(fk_equipo=planilla.fk_local, hombre=True)
	j_visita = Perfiles.objects.filter(fk_equipo=planilla.fk_visita, hombre=True)
	try:
		r_local = Perfiles.objects.get(fk_equipo=planilla.fk_local, hombre=True, representante=True)
	except:
		r_local = None
	try:
		c_local = Perfiles.objects.get(fk_equipo=planilla.fk_local, hombre=True, capitan=True)
	except:
		c_local = None
	try:
		r_visita = Perfiles.objects.get(fk_equipo=planilla.fk_visita, hombre=True, representante=True)
	except:
		r_visita = None
	try:
		c_visita = Perfiles.objects.get(fk_equipo=planilla.fk_visita, hombre=True, capitan=True)
	except:
		c_visita = None
	ctx = {'planilla':planilla, 'torneos':torneos, 'j_local':j_local, 'j_visita':j_visita, 'r_local':r_local, 'r_visita':r_visita, 'c_local':c_local, 'c_visita':c_visita}
	return render_to_response('print_planilla.html', ctx, context_instance=RequestContext(request))


def print_encuentro_mujeres_view(request, id_encuentro):
	torneos = Campeonato.objects.filter(estado=True)
	planilla = Encuentro.objects.get(id=id_encuentro)
	j_local	= Perfiles.objects.filter(fk_equipo=planilla.fk_local, mujer=True)
	j_visita = Perfiles.objects.filter(fk_equipo=planilla.fk_visita, mujer=True)
	try:
		r_local = Perfiles.objects.get(fk_equipo=planilla.fk_local, mujer=True, representante=True)
	except:
		r_local = None
	try:
		c_local = Perfiles.objects.get(fk_equipo=planilla.fk_local, mujer=True, capitan=True)
	except:
		c_local = None
	try:
		r_visita = Perfiles.objects.get(fk_equipo=planilla.fk_visita, mujer=True, representante=True)
	except:
		r_visita = None
	try:
		c_visita = Perfiles.objects.get(fk_equipo=planilla.fk_visita, mujer=True, capitan=True)
	except:
		c_visita = None
	ctx = {'planilla':planilla, 'torneos':torneos, 'j_local':j_local, 'j_visita':j_visita, 'r_local':r_local, 'r_visita':r_visita, 'c_local':c_local, 'c_visita':c_visita}
	return render_to_response('print_planilla.html', ctx, context_instance=RequestContext(request))


def print_carnet_view(request, id_carnet):
	torneos = Campeonato.objects.filter(estado=True)
	carnet = Perfiles.objects.get(id=id_carnet)
	ctx = {'carnet':carnet, 'torneos':torneos}
	return render_to_response('print_carnet.html', ctx, context_instance=RequestContext(request))

#reportes en pdf reporlab
from cStringIO import StringIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse

from io import BytesIO
from django.http import HttpResponse
from django.views.generic import ListView
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
#FIN reportes en pdf reporlab 
 
class IndexView(ListView):
    template_name = "print_c.html"
    model = Perfiles
    context_object_name = "c"
 
def generar_pdf(request):
    #print "Genero el PDF"
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "carnet.pdf"  # llamado clientes
    # la linea 26 es por si deseas descargar el pdf a tu computadora
    # response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=letter,
                            rightMargin=40,
                            leftMargin=40,
                            topMargin=60,
                            bottomMargin=18,
                            )
    clientes = []
    styles = getSampleStyleSheet()
    header = Paragraph("Listado de Jugadores", styles['Heading1'])
    clientes.append(header)
    headings = ('Cedula', 'Nombre', 'Apellidos', 'Correo')
    allclientes = [( p.cedula, p.nombres, p.apellidos, p.correo) for p in Perfiles.objects.all()]
    #print allclientes
 
    t = Table([headings] + allclientes)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (3, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))
    clientes.append(t)
    doc.build(clientes)
    response.write(buff.getvalue())
    buff.close()
    return response