from django.shortcuts import render, render_to_response
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator,EmptyPage,InvalidPage
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
	if request.method=='POST':
		formulario = ContactoForm(request.POST)
		if formulario.is_valid():
			titulo = 'Mesaje del Campeonato CIS-UNL_2015'
			contenido = formulario.cleaned_data['mensaje']+"\n"
			contenido += 'Comunicarse a: ' + formulario.cleaned_data['correo']
			correo = EmailMessage(titulo, contenido, to=['yrramirezs@unl.edu.ec'])
			try:
				correo.send()
			except Exception, e:
				return HttpResponseRedirect('/')
	else:
		formulario = ContactoForm()
	return render_to_response('contactenos.html',{'formulario':formulario, 'torneos':torneos}, context_instance=RequestContext(request))

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
		return render_to_response('jugadores.html',{'torneos':torneos,'pro':pro }, context_instance=RequestContext(request))

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

	ctx = {'jugadores':jugadores, 'torneos': torneos, 'equipos':equipos, 'perfil':perfil}
	return render_to_response('jugadores.html', ctx, context_instance=RequestContext(request))

def calendario_view(request,pagina):
  torneos = Campeonato.objects.filter(estado=True)
  #encuentros = Encuentro.objects.filter(fk_local__fk_campeonato__estado__exact=True).order_by('fk_fecha')
  encuentros = Encuentro.objects.filter(jugado__exact=False).order_by('fk_fecha')
  #PAGINACION
  paginator = Paginator(encuentros,5)
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

#@login_required(login_url='/ingresar')
def registrar_view(request):
	torneos = Campeonato.objects.filter(estado=True)
	info = "inicializando"
	if request.method == "POST":
		form = UserForm(request.POST)
		if form.is_valid():
			form.save()
			info = "Registrado Satisfactoriamente!!"
			ctx = {'info':info,'torneos':torneos}
			return render_to_response('agregar_jugador.html',ctx, context_instance=RequestContext(request))
	else:
		form = UserForm()
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

def equipos_view(request,pagina):
	jugadores = Perfiles.objects.filter(fk_equipo__fk_campeonato__estado__exact=True)
	torneos = Campeonato.objects.filter(estado=True)
	equipos = Equipo.objects.filter(fk_campeonato__estado__exact=True)

	#PAGINACION
	paginator = Paginator(jugadores,7)
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

