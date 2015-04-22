# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_encuentro_jugado'),
    ]

    operations = [
        migrations.AddField(
            model_name='juegotarjeta',
            name='pagado',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
