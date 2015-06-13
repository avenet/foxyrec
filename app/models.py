# -*- coding: utf-8 -*-
import uuid

from django.db import models


class Usuario(models.Model):
    SEXO = (
        (1, 'Mujer'),
        (2, 'Hombre')
    )

    RANGO_ETAREO = (
        (1, 'Menor a 15 años'),
        (2, '15 a 20 años'),
        (3, '21 a 30 años'),
        (4, '31 a 40 años'),
        (5, '41 a 50 años'),
        (6, '51 a 60 años'),
        (7, 'más de 60 años')
    )

    sexo = models.IntegerField(choices=SEXO)
    edad = models.IntegerField(choices=RANGO_ETAREO)
    user_id = models.CharField(default=uuid.uuid4, editable=False,
                               max_length=200)


class Item(models.Model):
    foto = models.URLField()
    descripcion = models.CharField(max_length=200)
    activo = models.BooleanField(default=True)
    valido = models.BooleanField(default=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        return super(Item, self).save(force_insert, force_update, using, update_fields)


class Seleccion(models.Model):
    usuario = models.ForeignKey('Usuario')
    item = models.ForeignKey('Item')
    me_gusta = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)
