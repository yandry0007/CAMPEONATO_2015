from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('campeonato.apps.main.views',
    # Examples:
    # url(r'^$', 'campeonato.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'index_view', name='vista_index'),
    url(r'^ingresar/$', 'ingresar_view', name='vista_ingresar'),
    url(r'^goleadores/$', 'goleadores_view', name='vista_goleadores'),
    url(r'^print/goleadores/$', 'print_goleadores_view', name='vista_print_goleadores'),
    url(r'^amonestados/$', 'amonestados_view', name='vista_amonestados'),
    url(r'^contactenos/$', 'contactenos_view', name='vista_contactenos'),
    url(r'^registrar/$', 'registrar_view', name='vista_registrar'),
    url(r'^salir/$', 'salir_view', name='vista_salir'),
    url(r'^agregar/perfil/$', 'agregar_perfil_view', name='vista_agregar_perfil'),

    url(r'^jugador/page/(?P<id_jugador>.*)/$', 'single_jugador_view', name='vista_single_jugador'),
    
    url(r'^resultados/page/(?P<pagina>.*)/$', 'resultados_view', name='vista_resultados'),
    url(r'^jugadores/page/(?P<pagina>.*)/$', 'jugadores_view', name='vista_jugadores'),
    url(r'^equipos/page/(?P<pagina>.*)/$', 'equipos_view', name='vista_equipos'),
    url(r'^calendarios/page/(?P<pagina>.*)/$', 'calendario_view', name='vista_calendarios'),

)
