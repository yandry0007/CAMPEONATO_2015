from django.conf.urls import patterns, include, url
from django.contrib import admin
from campeonato.apps.main.views import IndexView

urlpatterns = patterns('campeonato.apps.main.views',
    # Examples:
    # url(r'^$', 'campeonato.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'index_view', name='vista_index'),
    url(r'^ingresar/$', 'ingresar_view', name='vista_ingresar'),
    url(r'^goleadores/$', 'goleadores_view', name='vista_goleadores'),
    url(r'^amonestados/$', 'amonestados_view', name='vista_amonestados'),
    url(r'^contactenos/$', 'contactenos_view', name='vista_contactenos'),
    url(r'^registrar/$', 'registrar_view', name='vista_registrar'),
    url(r'^salir/$', 'salir_view', name='vista_salir'),

    url(r'^agregar/perfil/$', 'agregar_perfil_view', name='vista_agregar_perfil'),
    #url(r'^agregar/perfil/$', agregarPerfil.as_view() , name='vista_agregar_perfil'),

    url(r'^jugador/page/(?P<id_jugador>.*)/$', 'single_jugador_view', name='vista_single_jugador'),
    url(r'^resultados/page/(?P<pagina>.*)/$', 'resultados_view', name='vista_resultados'),
    url(r'^jugadores/page/(?P<pagina>.*)/$', 'jugadores_view', name='vista_jugadores'),
    url(r'^equipos/page/(?P<pagina>.*)/$', 'equipos_view', name='vista_equipos'),
    url(r'^calendarios/page/varones/(?P<pagina>.*)/$', 'calendario_varones_view', name='vista_calendarios_varones'),
    url(r'^calendarios/page/mujeres/(?P<pagina>.*)/$', 'calendario_mujeres_view', name='vista_calendarios_mujeres'),
    url(r'^print/goleadores/$', 'print_goleadores_view', name='vista_print_goleadores'),
    url(r'^print/plantilla/$', 'print_plantilla_view', name='vista_print_plantilla'),
    url(r'^print/encuentro/varones/(?P<id_encuentro>.*)/$', 'print_encuentro_varones_view', name='vista_print_encuentro_varones'),
    url(r'^print/encuentro/mujeres/(?P<id_encuentro>.*)/$', 'print_encuentro_mujeres_view', name='vista_print_encuentro_mujeres'),
    url(r'^print/carnet/(?P<id_carnet>.*)/$', 'print_carnet_view', name='vista_print_carnet'),
    
    #URLS PARA PDFs
    url(r'^print_c/$', IndexView.as_view(), name='home'),
    url(r'^generar_pdf/$', 'generar_pdf', name='pdf'),

)
