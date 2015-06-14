# -*- coding: utf-8 -*-
import json
import httplib2

from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import SeleccionForm, UsuarioForm
from .models import Item, Usuario


@login_required
def inicio(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)

        if form.is_valid():
            user = form.save(commit=True)
            form.instance.usuario = request.user
            form.instance.save()
            return redirect("loop", user_id=user.user_id)
        else:
            print form.errors
    else:
        try:
            request_user = Usuario.objects.get(usuario__pk=request.user.pk)
            return redirect("loop", user_id=request_user.user_id)
        except Usuario.DoesNotExist:
            form = UsuarioForm()

    return render(request, 'add_user.html', {
        'form': form
    })


@login_required
def loop(request, user_id):
    foto = ""
    desc = ""

    if request.method == 'POST':
        form = SeleccionForm(request.POST)

        if form.is_valid():
            item_id = request.POST['item']

            me_gusta = True

            if 'dislike' in request.POST:
                me_gusta = False
            elif 'skip' in request.POST:
                me_gusta = None

            usuario = Usuario.objects.filter(user_id=user_id).first()

            item = Item.objects.get(pk=item_id)

            form = form.save(commit=False)

            form.usuario = usuario
            form.item = item
            form.me_gusta = me_gusta
            form.save()

            return redirect("loop", user_id=usuario.user_id)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        item_id = _get_prediction_item(user_id)
        item = Item.objects.get(pk=item_id)
        foto = item.foto
        desc = item.descripcion
        form = SeleccionForm(initial={'usuario': user_id, 'item': item.pk})

    return render(request, 'loop.html', {
        'form': form,
        'foto': foto,
        'desc': desc
    })


def _get_prediction_item(user_id):
    usuario = Usuario.objects.get(user_id=user_id)

    client_email = settings.GOOGLE_PREDICTIONS_CLIENT_EMAIL
    private_key = settings.GOOGLE_PREDICTIONS_PRIVATE_KEY

    credentials = SignedJwtAssertionCredentials(client_email, private_key, settings.GOOGLE_PREDICTIONS_URL)

    sexo = usuario.sexo == 1 and 'Mujer' or 'Hombre'
    edad = usuario.edad

    query = "Me gusta, {}, Menor a {} años".format(sexo, edad)

    http = httplib2.Http()
    http = credentials.authorize(http)

    service = build('prediction', 'v1.6', http=http)
    result = service.trainedmodels().predict(
        id='model001',
        project='foxyrec-demo',
        prettyPrint='true',
        fields='outputLabel',
        body={
            'input': {
                'csvInstance': [str(query)]
            }
        }
    ).execute()

    identifier_info = result['outputLabel']

    cleaned_id_info = identifier_info.replace('"', '')

    item_id = cleaned_id_info.split(':')

    if len(item_id) > 1:
        return int(item_id[1])

    return None