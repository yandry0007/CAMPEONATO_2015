from django.db import models
from django.contrib.auth.models import User

class Campeonato(models.Model):
	nombre = models.CharField(max_length=200)
	estado = models.BooleanField(blank=False, default=False)
	fk_organizador = models.ForeignKey(User)

	class Meta:
	    verbose_name = 'Campeonato'
	    verbose_name_plural = 'Campeonatos'

	def __unicode__(self):
		return self.nombre

class Resultado(models.Model):
	resultado = models.CharField(blank=False, max_length=50)
	class Meta:
	    verbose_name = 'Resultado'
	    verbose_name_plural = 'Resultados'
	def __unicode__(self):
		return self.resultado

class Equipo(models.Model):
	nombre = models.CharField(max_length=200)
	inscripcion = models.BooleanField(blank=False, default=False)
	puntos = models.IntegerField(blank=True, default="0")
	gf = models.IntegerField(blank=False, default="0")
	gc = models.IntegerField(blank=False, default="0")
	pj = models.IntegerField(blank=False, default="0")
	pg = models.IntegerField(blank=False, default="0")
	pe = models.IntegerField(blank=False, default="0")
	pp = models.IntegerField(blank=False, default="0")
	fk_campeonato = models.ForeignKey(Campeonato)

	class Meta:
	    verbose_name = 'Equipo'
	    verbose_name_plural = 'Equipos'

	def __unicode__(self):
		return '%s - %s' %(self.nombre,self.fk_campeonato)

class Ternaria_arbitros(models.Model):
	arbitro = models.CharField(max_length=200)
	correo = models.EmailField(blank=False)
	
	class Meta:
	    verbose_name = 'Arbitro'
	    verbose_name_plural = 'Arbitros'

	def __unicode__(self):
		return "%s - %s" %(self.arbitro, self.correo)

class Grupos(models.Model):
	nombre = models.CharField(max_length=200)
	equipos = models.ManyToManyField(Equipo)

	class Meta:
	    verbose_name = 'Grupo'
	    verbose_name_plural = 'Grupos'

	def __unicode__(self):
		return self.nombre


tipos_estaturas = (('bajo','1.40'),('bajo','1.42'),('bajo','1.44'),
    ('bajo','1.46'),('bajo','1.48'),('bajo','1.50'),('bajo','1.52'),
    ('bajo','1.54'),('bajo','1.56'),('bajo','1.58'),('medio','1.60'),
    ('medio','1.62'),('medio','1.64'),('medio','1.66'),('medio','1.68'),
    ('medio','1.70'),('alto','1.72'),('alto','1.74'),('alto','1.76'),
    ('alto','1.78'),('alto','1.80'),('alto','1.82'),('alto','1.84'),
    ('alto','1.86'),('alto','1.88'),('alto','1.90'),('alto','1.92')
)

def url(self, filename):
	ruta = "static/img/Perfiles/%s/%s"%(self.user.username,str(filename))
	return ruta 


class Perfiles(models.Model):
	user = models.OneToOneField(User)
	nombres = models.CharField(blank=False, max_length=30)
	apellidos = models.CharField(blank=False, max_length=30)
	cedula = models.IntegerField(blank=False, unique=True)
	representante = models.BooleanField(blank=False, default=False)
	capitan = models.BooleanField(blank=False, default=False)
	foto = models.ImageField(upload_to=url)
	estatura = models.CharField( max_length='20', choices=tipos_estaturas)
	correo = models.EmailField(blank=False)
	telefono = models.IntegerField(blank=False, max_length=30)
	fk_equipo = models.ForeignKey(Equipo)
	
	def __unicode__(self):
		return self.user.username

	class Meta:
		verbose_name = 'Perfil'
		verbose_name_plural = 'Perfiles'

class Goles(models.Model):
	goles = models.IntegerField(blank=False, default="0")
	fk_user = models.ForeignKey(Perfiles)
	
	class Meta:
	    verbose_name = 'Gol'
	    verbose_name_plural = 'Goles'
	
	def __unicode__(self):
		return '%s - %s' %(self.goles, self.fk_user)



class Fecha(models.Model):
	fecha = models.CharField(blank=False, max_length=50)
	class Meta:
	    verbose_name = 'Fecha'
	    verbose_name_plural = 'Fechas'
	def __unicode__(self):
		return self.fecha

class Fase(models.Model):
	fase = models.CharField(max_length=200)
	status = models.BooleanField(blank=False, default=False)

	class Meta:
	    verbose_name = 'Fase'
	    verbose_name_plural = 'Fases'
	
	def __unicode__(self):
		return self.fase

class Encuentro(models.Model):
	hora = models.DateTimeField()
	cancha = models.CharField(max_length=200)
	fk_arbitros = models.ForeignKey(Ternaria_arbitros)
	fk_local = models.ForeignKey(Equipo, related_name='+')
	fk_visita = models.ForeignKey(Equipo, related_name='+')
	fk_fecha = models.ForeignKey(Fecha)
	fk_fase = models.ForeignKey(Fase)
	goleslocal = models.IntegerField(blank=False, default="0")
	golesvisita = models.IntegerField(blank=False, default="0")
  	jugado = models.BooleanField(blank=False, default=False)
  
	class Meta:
	    verbose_name = 'Encuentro'
	    verbose_name_plural = 'Encuentros'
	
	def __unicode__(self):
		return '%s - %s vs %s' %(self.fk_fecha, self.fk_local, self.fk_visita)

class Tarjeta(models.Model):
	tarjeta = models.CharField(blank=False, max_length=50)
	fk_tarjetas = models.ManyToManyField(Perfiles, through='JuegoTarjeta')
	
	class Meta:
	    verbose_name = 'Tarjeta'
	    verbose_name_plural = 'Tarjetas'
	
	def __unicode__(self):
		return self.tarjeta

class JuegoTarjeta(models.Model):
	fk_tarjeta = models.ForeignKey(Tarjeta)
	fk_juego = models.ForeignKey(Encuentro)
	fk_jugador = models.ForeignKey(Perfiles)
  	pagado = models.BooleanField(blank=False, default=False)
	
	class Meta:
	    verbose_name = 'Amonestado'
	    verbose_name_plural = 'Amonestados'
	def __unicode__(self):
		return '%s %s %s' %(self.fk_tarjeta, self.fk_juego, self.fk_jugador)


