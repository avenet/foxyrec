# -*- coding: utf-8 -*-
import json
import httplib2

from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import SeleccionForm, UsuarioForm
from .models import Item, Usuario, Seleccion


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

            seleccion = form.save(commit=False)

            seleccion.usuario = usuario
            seleccion.item = item
            seleccion.me_gusta = me_gusta
            seleccion.save()

            _update_prediction_item(seleccion.id)

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

    credentials = SignedJwtAssertionCredentials(client_email, private_key,
                                                settings.GOOGLE_PREDICTIONS_URL)

    sexo = usuario.sexo == 1 and 'Mujer' or 'Hombre'
    edad = _get_edad_string(usuario.edad)

    query = "Me gusta, {}, {}".format(sexo, edad)

    http = httplib2.Http()
    http = credentials.authorize(http)

    service = build('prediction', 'v1.6', http=http)
    result = service.trainedmodels().predict(
        id='model001',
        project='foxyrec-demo',
        prettyPrint='true',
        fields='outputMulti',
        body={
            'input': {
                'csvInstance': [str(query)]
            }
        }
    ).execute()

    output_multi = result['outputMulti']
    output_multi.sort(key=lambda x: x['score'])



    # Check latest item for user X
    id_ultima_seleccion = None

    selecciones_usuario = Seleccion.objects.filter(
        usuario=usuario).order_by('-pk')[0:1]

    result_item = None
    
    if selecciones_usuario:
        id_ultima_seleccion = selecciones_usuario[0].pk

    if not id_ultima_seleccion:
        result_item = output_multi[0]
    else:
        item_label = 'ID:{}'.format(id_ultima_seleccion)
        for i in xrange(len(output_multi)):
            current_item = output_multi[i]
            if current_item['label'] == item_label:
                result_item = output_multi[(i + 1) % len(output_multi)]
                break

    # Label del item
    identifier_info = result_item['label']

    cleaned_id_info = identifier_info.replace('"', '')

    item_id = cleaned_id_info.split(':')

    if len(item_id) > 1:
        return int(item_id[1])

    return None


def _update_prediction_item(seleccion_id):
    seleccion = Seleccion.objects.get(pk=seleccion_id)

    client_email = settings.GOOGLE_PREDICTIONS_CLIENT_EMAIL
    private_key = settings.GOOGLE_PREDICTIONS_PRIVATE_KEY

    credentials = SignedJwtAssertionCredentials(client_email, private_key,
                                                settings.GOOGLE_PREDICTIONS_URL)

    sexo = seleccion.usuario.sexo == 1 and 'Mujer' or 'Hombre'
    edad = _get_edad_string(seleccion.usuario.edad)
    item = "ID:" + str(seleccion.item.pk)
    like = seleccion.me_gusta == 1 and 'Me gusta' or 'No me gusta'

    query = "{}, {}, {}, {}".format(item, like, sexo, edad)

    http = httplib2.Http()
    http = credentials.authorize(http)

    service = build('prediction', 'v1.6', http=http)
    service.trainedmodels().update(id='model001', project='foxyrec-demo',
                                   body={'output': '',
                                         'csvInstance': [str(query)]}).execute()

    return None


def _get_edad_string(edad):
    edades = {
        1: 'Menor a 15 años',
        2: '15 a 20 años',
        3: '21 a 30 años',
        4: '31 a 40 años',
        5: '41 a 50 años',
        6: '51 a 60 años',
        7: 'más de 60 años',
    }
    return edades[edad]
