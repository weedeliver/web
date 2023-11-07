from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from web.models import Produktua, Kategoria, Bezeroa, Saskia, SaskiaItem


# Create your views here.
def index(request):
    return render(request, 'index.html')


def produktuak(request):
    produktuak = Produktua.objects.all()
    kategoriak = Kategoria.objects.all()
    if request.user.is_authenticated:
        user = request.user
        bezeroa = Bezeroa.objects.get(user=user)
        return render(request, 'produktuak.html', {'produktuak': produktuak, 'kategoriak': kategoriak, 'bezeroa': bezeroa})
    else:
        return render(request, 'produktuak.html', {'produktuak': produktuak, 'kategoriak': kategoriak})


def produktuak_kategoria(request, cat):
    produktuak = Produktua.objects.filter(izena=cat)
    kategoriak = Kategoria.objects.all()
    aukeratutako_kategoria = Kategoria.objects.get(izena=cat)
    if request.user.is_authenticated:
        user = request.user
        bezeroa = Bezeroa.objects.get(user=user)
        return render(request, 'produktuak.html', {'produktuak': produktuak, 'kategoriak': kategoriak, 'aukeratutako_kategoria': aukeratutako_kategoria, 'bezeroa': bezeroa})
    else:
        return render(request, 'produktuak.html', {'produktuak': produktuak, 'kategoriak': kategoriak, 'aukeratutako_kategoria': aukeratutako_kategoria})


def produktua(request, pid):
    produktua = Produktua.objects.get(id=pid)
    kategoriak = Produktua.objects.filter(id=pid).values('kategoria__izena')
    user = request.user
    bezeroa = Bezeroa.objects.get(user=user)
    return render(request, 'produktua.html', {'produktua': produktua, 'kategoriak': kategoriak})


def kontaktua(request):
    return render(request, 'kontaktua.html')


def login_view(request):
    return render(request, 'login.html')


def signup_view(request):
    return render(request, 'signup.html')


def kontua_sortu(request):
    # get the data
    izena = request.POST['izena']
    abizena = request.POST['abizena']
    emaila = request.POST['email']
    telefonoa = request.POST['telefonoa']
    pasahitza = request.POST['pasahitza']
    pasahitza2 = request.POST['pasahitza2']
    # verify the two passwords are the same
    if pasahitza == pasahitza2:
        # create the user
        user = User.objects.create_user(username=emaila, password=pasahitza)
        user.save()
        # create the client and tie it to the user
        bezeroa = Bezeroa(user=user, izena=izena, abizena=abizena, emaila=emaila, telefonoa=telefonoa, harpidetza="basic")
        bezeroa.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponseRedirect(reverse('signup'))


def auth(request):
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
        # Log the user in
        user = form.get_user()
        login(request, user)  # Pass the request and user to login
        return HttpResponseRedirect(reverse('index'))
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form, 'error': 'Erabiltzaile edo pasahitz okerra.'})


@login_required
def logout_view(request):
    # log out the user and redirect to the index page
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def kontua(request):
    user = request.user
    bezeroa = Bezeroa.objects.get(user=user)
    return render(request, 'kontua.html', {'bezeroa': bezeroa})


@login_required
def kontua_aldatu(request):
    user = request.user
    bezeroa = Bezeroa.objects.get(user=user)
    return render(request, 'kontua_aldatu.html', {'bezeroa': bezeroa})


def plus(request):
    user = request.user
    bezeroa = Bezeroa.objects.get(user=user)
    return render(request, 'plus.html', {'bezeroa': bezeroa})


@login_required
def harpidetu(request):
    harpidetza = request.POST['harpidetza']
    user = request.user
    bezeroa = Bezeroa.objects.get(user=user)
    bezeroa.harpidetza = harpidetza
    bezeroa.save()
    return render(request, 'kontua.html', {'bezeroa': bezeroa, 'planberria': harpidetza})


@login_required
def kontua_aldaketak_gorde(request):
    user = request.user
    bezeroa = Bezeroa.objects.get(user=user)
    # get the data
    izena = request.POST['izena']
    abizena = request.POST['abizena']
    emaila = request.POST['email']
    telefonoa = request.POST['telefonoa']
    helbidea = request.POST['helbidea']
    herria = request.POST['herria']
    posta_kodea = request.POST['posta_kodea']
    txartela = request.POST['txartela']
    # update bezeroa
    bezeroa.izena = izena
    bezeroa.abizena = abizena
    bezeroa.emaila = emaila
    bezeroa.telefonoa = telefonoa
    bezeroa.helbidea = helbidea
    bezeroa.herria = herria
    bezeroa.posta_kodea = posta_kodea
    bezeroa.txartela = txartela
    bezeroa.save()
    return render(request, 'kontua.html', {'bezeroa': bezeroa})


def saskia_view(request):
    user = request.user
    bezeroa = Bezeroa.objects.get(user=user)
    saskia = Saskia.objects.filter(bezeroa=bezeroa).first()
    items = SaskiaItem.objects.filter(saskia=saskia)
    return render(request, 'saskia.html', {'items': items, 'bezeroa': bezeroa})


def saskira_gehitu(request, pid):
    produktua_obj = Produktua.objects.get(id=pid)
    kantitatea = int(request.POST['kantitatea'])
    user = request.user
    bezeroa = Bezeroa.objects.get(user=user)
    saskia = Saskia.objects.filter(bezeroa=bezeroa).first()

    # Saski bat sortu ez bada existitzen
    if saskia is None:
        saskia = Saskia()
        saskia.bezeroa = bezeroa
        saskia.save()

    duplicate_item = saskia.saskia_items.filter(produktua=produktua_obj, saskia=saskia).first()
    if duplicate_item is not None:
        duplicate_item.kantitatea += kantitatea
        duplicate_item.save()
    else:
        saskia_item = SaskiaItem()
        saskia_item.produktua = produktua_obj
        saskia_item.kantitatea = kantitatea
        saskia_item.saskia = saskia
        saskia_item.save()
        saskia.saskia_items.add(saskia_item)

    return HttpResponseRedirect(reverse('saskia'))
