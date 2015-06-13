from random import randint

from django.shortcuts import render, redirect

from .forms import SeleccionForm, UsuarioForm
from .models import Item, Usuario


def inicio(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = UsuarioForm(request.POST)

        if form.is_valid():
            user = form.save(commit=True)
            return redirect("loop", user_id=user.user_id)
        else:
            print form.errors
    else:
        form = UsuarioForm()

    return render(request, 'add_user.html', {
        'form': form
    })


def loop(request, user_id):
    # A HTTP POST?
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
        count = Item.objects.all().count() - 1
        rand = randint(0, count)
        item = Item.objects.all()[rand]
        foto = item.foto
        desc = item.descripcion
        form = SeleccionForm(initial={'usuario': user_id, 'item': item.pk})

    return render(request, 'loop.html', {
        'form': form,
        'foto': foto,
        'desc': desc
    })
