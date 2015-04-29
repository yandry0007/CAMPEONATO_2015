# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import campeonato.apps.main.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Campeonato',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
                ('estado', models.BooleanField(default=False)),
                ('fk_organizador', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Campeonato',
                'verbose_name_plural': 'Campeonatos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Disciplina',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'Disciplina',
                'verbose_name_plural': 'Disciplinas',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Encuentro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hora', models.DateTimeField()),
                ('cancha', models.CharField(max_length=200)),
                ('goleslocal', models.IntegerField(default=b'0')),
                ('golesvisita', models.IntegerField(default=b'0')),
                ('jugado', models.BooleanField(default=False)),
                ('varones', models.BooleanField(default=False)),
                ('mujeres', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Encuentro',
                'verbose_name_plural': 'Encuentros',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Equipo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
                ('inscripcion', models.BooleanField(default=False)),
                ('puntos', models.IntegerField(default=b'0', blank=True)),
                ('gf', models.IntegerField(default=b'0')),
                ('gc', models.IntegerField(default=b'0')),
                ('pj', models.IntegerField(default=b'0')),
                ('pg', models.IntegerField(default=b'0')),
                ('pe', models.IntegerField(default=b'0')),
                ('pp', models.IntegerField(default=b'0')),
                ('fk_campeonato', models.ForeignKey(to='main.Campeonato')),
            ],
            options={
                'verbose_name': 'Equipo',
                'verbose_name_plural': 'Equipos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Fase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fase', models.CharField(max_length=200)),
                ('status', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Fase',
                'verbose_name_plural': 'Fases',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Fecha',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Fecha',
                'verbose_name_plural': 'Fechas',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Goles',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('goles', models.IntegerField(default=b'0')),
            ],
            options={
                'verbose_name': 'Gol',
                'verbose_name_plural': 'Goles',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Grupos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
                ('equipos', models.ManyToManyField(to='main.Equipo')),
            ],
            options={
                'verbose_name': 'Grupo',
                'verbose_name_plural': 'Grupos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='JuegoTarjeta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pagado', models.BooleanField(default=False)),
                ('fk_juego', models.ForeignKey(to='main.Encuentro')),
            ],
            options={
                'verbose_name': 'Amonestado',
                'verbose_name_plural': 'Amonestados',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Perfiles',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombres', models.CharField(max_length=30)),
                ('apellidos', models.CharField(max_length=30)),
                ('cedula', models.IntegerField(unique=True)),
                ('representante', models.BooleanField(default=False)),
                ('capitan', models.BooleanField(default=False)),
                ('foto', models.ImageField(upload_to=campeonato.apps.main.models.url)),
                ('estatura', models.CharField(max_length=b'20', choices=[(b'bajo', b'1.40'), (b'bajo', b'1.42'), (b'bajo', b'1.44'), (b'bajo', b'1.46'), (b'bajo', b'1.48'), (b'bajo', b'1.50'), (b'bajo', b'1.52'), (b'bajo', b'1.54'), (b'bajo', b'1.56'), (b'bajo', b'1.58'), (b'medio', b'1.60'), (b'medio', b'1.62'), (b'medio', b'1.64'), (b'medio', b'1.66'), (b'medio', b'1.68'), (b'medio', b'1.70'), (b'alto', b'1.72'), (b'alto', b'1.74'), (b'alto', b'1.76'), (b'alto', b'1.78'), (b'alto', b'1.80'), (b'alto', b'1.82'), (b'alto', b'1.84'), (b'alto', b'1.86'), (b'alto', b'1.88'), (b'alto', b'1.90'), (b'alto', b'1.92')])),
                ('correo', models.EmailField(max_length=75)),
                ('telefono', models.IntegerField(max_length=30)),
                ('hombre', models.BooleanField(default=False)),
                ('mujer', models.BooleanField(default=False)),
                ('fk_equipo', models.ForeignKey(to='main.Equipo')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Perfil',
                'verbose_name_plural': 'Perfiles',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Resultado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('resultado', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Resultado',
                'verbose_name_plural': 'Resultados',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tarjeta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tarjeta', models.CharField(max_length=50)),
                ('fk_tarjetas', models.ManyToManyField(to='main.Perfiles', through='main.JuegoTarjeta')),
            ],
            options={
                'verbose_name': 'Tarjeta',
                'verbose_name_plural': 'Tarjetas',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ternaria_arbitros',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('arbitro', models.CharField(max_length=200)),
                ('correo', models.EmailField(max_length=75)),
            ],
            options={
                'verbose_name': 'Arbitro',
                'verbose_name_plural': 'Arbitros',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='juegotarjeta',
            name='fk_jugador',
            field=models.ForeignKey(to='main.Perfiles'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='juegotarjeta',
            name='fk_tarjeta',
            field=models.ForeignKey(to='main.Tarjeta'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='goles',
            name='fk_user',
            field=models.ForeignKey(to='main.Perfiles'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='encuentro',
            name='fk_arbitros',
            field=models.ForeignKey(to='main.Ternaria_arbitros'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='encuentro',
            name='fk_disciplina',
            field=models.ForeignKey(to='main.Disciplina'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='encuentro',
            name='fk_fase',
            field=models.ForeignKey(to='main.Fase'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='encuentro',
            name='fk_fecha',
            field=models.ForeignKey(to='main.Fecha'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='encuentro',
            name='fk_local',
            field=models.ForeignKey(related_name='+', to='main.Equipo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='encuentro',
            name='fk_visita',
            field=models.ForeignKey(related_name='+', to='main.Equipo'),
            preserve_default=True,
        ),
    ]
