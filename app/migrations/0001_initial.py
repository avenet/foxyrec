# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('foto', models.URLField()),
                ('descripcion', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Seleccion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('me_gusta', models.BooleanField()),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('item', models.ForeignKey(to='app.Item')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sexo', models.IntegerField(choices=[(1, b'Mujer'), (2, b'Hombre')])),
                ('edad', models.IntegerField(choices=[(1, b'Menor a 15 a\xc3\xb1os'), (2, b'15 a 20 a\xc3\xb1os'), (3, b'21 a 30 a\xc3\xb1os'), (4, b'31 a 40 a\xc3\xb1os'), (5, b'41 a 50 a\xc3\xb1os'), (6, b'51 a 60 a\xc3\xb1os'), (7, b'm\xc3\xa1s de 60 a\xc3\xb1os')])),
                ('user_id', models.CharField(default=uuid.uuid4, max_length=200, editable=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='seleccion',
            name='usuario',
            field=models.ForeignKey(to='app.Usuario'),
            preserve_default=True,
        ),
    ]
