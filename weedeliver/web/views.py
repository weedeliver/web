import random
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from web.models import Erosketa, Produktua, Kategoria, Bezeroa, Saskia, SaskiaItem


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
    produktuak = Produktua.objects.all().filter(kategoria__izena=cat)
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
    if request.user.is_authenticated:
        user = request.user
        bezeroa = Bezeroa.objects.get(user=user)
        return render(request, 'produktua.html', {'produktua': produktua, 'kategoriak': kategoriak})
    else:
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
    erosketak = Erosketa.objects.filter(bezeroa=bezeroa)
    return render(request, 'kontua.html', {'bezeroa': bezeroa,'erosketak':erosketak})


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
        saskia_item.prezioa_deskontua = produktua_obj.prezioa
        if saskia_item.produktua.deskontua.izena != "Ez":
            if saskia_item.produktua.deskontua.isEhunekoa:
                saskia_item.prezioa_deskontua = saskia_item.produktua.prezioa - (saskia_item.produktua.prezioa * saskia_item.produktua.deskontua.kantitatea / 100)
            else:
                saskia_item.prezioa_deskontua = saskia_item.produktua.prezioa - saskia_item.produktua.deskontua.kantitatea
        saskia_item.saskia = saskia
        saskia_item.save()
        saskia.saskia_items.add(saskia_item)

    return HttpResponseRedirect(reverse('saskia'))


def unitateak_aldatu(request):
    product_id = request.POST['product_id']
    aldatu = request.POST['aldatu']
    produktua = Produktua.objects.get(id=product_id)
    user = request.user
    bezeroa = Bezeroa.objects.get(user=user)
    saskia = Saskia.objects.filter(bezeroa=bezeroa).first()

    ##Gehitu beharreko produktua aurkitu
    existing_item = SaskiaItem.objects.filter(produktua=produktua,saskia=saskia).first()
    ##Produktua karritoan badago unitate bat gehiago gehitu
    if existing_item and aldatu == "gehitu": 
        existing_item.kantitatea += 1
        existing_item.save()
    elif existing_item and aldatu == "kendu" and existing_item.kantitatea > 0:
        if existing_item.kantitatea != 1:
            existing_item.kantitatea -= 1
            existing_item.save()
        else:
            return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': False})

    if produktua.deskontua.izena != "Ez":
        if produktua.deskontua.isEhunekoa:
            data = [{'success': True,"prezioa": produktua.prezioa - (produktua.prezioa * produktua.deskontua.kantitatea / 100),"kantitatea": existing_item.kantitatea}]
        else:
            data = [{'success': True,"prezioa": produktua.prezioa - produktua.deskontua.kantitatea,"kantitatea": existing_item.kantitatea}]
    else:
        data = [{'success': True,"prezioa": produktua.prezioa,"kantitatea": existing_item.kantitatea}]
    return JsonResponse(data, safe=False)


@login_required
def saskitik_ezabatu(request):
    user = request.user
    bezeroa = Bezeroa.objects.get(user=user)
    saskia= Saskia.objects.filter(bezeroa=bezeroa).first()
    item_id = request.POST['item_id']
    ##Sortutako itema ezabatu
    item = SaskiaItem.objects.get(id=item_id,saskia=saskia)
    item.delete()

    total_items = SaskiaItem.objects.filter(saskia=saskia).count()
    data = [{'success': True,'items': total_items}]
    return JsonResponse(data,safe=False)


@login_required
def erosketa_egin(request):
    user = request.user
    bez = Bezeroa.objects.get(user=user)
    
    saskia = Saskia.objects.filter(bezeroa=bez).first()

    ##PRODUKTUAK GORDETZEKO
    guz = 0
    produktuak = []
    items = SaskiaItem.objects.filter(saskia=saskia)
    for i in items:
        produktua = i.produktua
        produktuak.append(produktua)
        guz = guz + (i.kantitatea * i.prezioa_deskontua)
    
    erosketa = Erosketa()
    erosketa.bezeroa = bez
    erosketa.totala = guz
    erosketa.save()  # Save the Erosketa object before setting the many-to-many relationship

    # Now, set the many-to-many relationship
    erosketa.produktuak.set(produktuak)

    ##saskia eta itemak ezabatu
    saskia.delete()
    items.delete()
    return HttpResponseRedirect(reverse('index'))


def gomendioak(request):
    gomendioak_produktuak = list(Produktua.objects.all())
    random_produktuak = random.sample(gomendioak_produktuak,10)

    data = [{"name": gomendioa.izena, "image": gomendioa.img.url} for gomendioa in random_produktuak]
    return JsonResponse(data, safe=False)
