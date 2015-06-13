# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20150613_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seleccion',
            name='me_gusta',
            field=models.NullBooleanField(default=False),
        ),
    ]
