from django.contrib import admin
from campeonato.apps.main.models import *


# class MembershipInline(admin.TabularInline): #StackedInline || TabularInline para agrupar mas los campos
#     model = Encuentro.fk_fase.through
#     extra = 2


class EquipoAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'fk_campeonato')
	search_fields = ['nombre']
	#raw_id_fields = ('inscripcion',) #permite a los usuarios buscar y seleccionar un valor
	#radio_fields = {"campeonato": admin.VERTICAL} #HORIZONTAL Sirve para poner en radio Button los datos ingresados
	#inlines  = [ InscripcionInline ,]
	#exclude = ('inscripcion',)


class EncuentroAdmin(admin.ModelAdmin):
	list_display = ('cancha', 'fk_arbitros', 'hora')
	#search_fields  =  [ 'cancha' ] #Campos a buscar
	list_filter  =  [ 'hora' ] #Filtra los datos a buscar por hora mes o anio
	#list_select_related = ('equipos', 'equipos')
	#raw_id_fields = ('equipos',)
	radio_fields = {"fk_arbitros": admin.VERTICAL}
	
	# inlines  = [ 
	# 	MembershipInline ,
	# ]
	# exclude = ('fk_fase',)

	#Sirve para personalizar el formulario al momento de ingresar los datos
	#fields = ['hora', 'cancha','arbitros', 'grupos','equipos']  
	#Para Dividir en partes diferentes los formularios de ingreso de datos
	fieldsets = [
		('Informacion de la Cancha', {'fields': ['cancha', 'fk_arbitros', 'fk_fase']} ),
        #('Infromacion de la Fecha y hora', {'fields': ['hora'], 'classes': ['collapse'] }),  #Collapse sirve para ocultar o mostrar (mas) 
        ('Infromacion de la Fecha y hora', {'fields': ['hora'] }),
    ]

	#inlines = [ ChoiceInline, ] #Agregar datos en forma de Choices

admin.site.register(Campeonato)
admin.site.register(Equipo)
admin.site.register(Encuentro)
admin.site.register(Ternaria_arbitros)
admin.site.register(Grupos)
admin.site.register(Fecha)
admin.site.register(Fase)
admin.site.register(Tarjeta)
admin.site.register(JuegoTarjeta)
admin.site.register(Resultado)
admin.site.register(Perfiles)
admin.site.register(Goles)
admin.site.register(Disciplina)