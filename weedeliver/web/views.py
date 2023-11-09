import random
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import Bezeroa,Kategoria,Produktua,Deskontua,Erosketa,Karrito,KarritoItem

# Create your views here.
def home(request):
    return render(request, 'home.html')

def kontaktua(request):

    return render(request,'kontaktua.html')

def produktuak(request):
    produktuak = Produktua.objects.all()
    kategoriak = Kategoria.objects.all()

    return render(request,'produktuak.html',{"produktuak":produktuak,"kategoriak":kategoriak})

def login_view(request):
    return render(request,'login.html')

def saioa_hasi(request):
    username = request.GET['erabiltzailea']
    password = request.GET['pasahitza']

    user = authenticate(request, username=username, password=password)
    print(user)
    if user is not None:
        login(request, user)  
        return JsonResponse({'redirect': reverse('home')})
    else:
        return JsonResponse({'error': 'Authentication failed'}, status=403)

def signup(request):
    return render(request,'signup.html')

def kontua_sortu(request):
    # get the data
    izena = request.POST['izena']
    abizena = request.POST['abizena']
    emaila = request.POST['email']
    telefonoa = request.POST['telefonoa']
    pasahitza = request.POST['pasahitza']
    pasahitza2 = request.POST['pasahitza2']
    helbidea = request.POST['helbidea']
    herria = request.POST['herria']
    posta = request.POST['posta']
    txartela = request.POST['txartela']
    # verify the two passwords are the same
    if pasahitza == pasahitza2:
        # create the user
        user = User.objects.create_user(username=emaila, password=pasahitza)
        user.save()
        # create the client and tie it to the user
        bezeroa = Bezeroa(user=user, izena=izena, abizena=abizena, emaila=emaila, telefonoa=telefonoa, helbidea=helbidea,herria=herria,posta_kodea=posta,txartela=txartela,harpidetza="basic")
        bezeroa.save()
        return HttpResponseRedirect(reverse('home'))
    else:
        return HttpResponseRedirect(reverse('signup'))
    
def profila(request):
    user = request.user
    bezeroa = Bezeroa.objects.get(user=user)

    erosketak = Erosketa.objects.filter(bezeroa=bezeroa)
    return render(request,'profila.html',{"bezeroa": bezeroa,"erosketak":erosketak})


@login_required
def saioa_itxi(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def karrito_view(request):
    user = request.user
    bezeroa = Bezeroa.objects.get(user=user)
    karrito = Karrito.objects.filter(bezeroa=bezeroa).first()
    items = KarritoItem.objects.filter(karrito=karrito)

    return render(request,'karrito.html',{"items":items,"karrito":karrito})

@login_required
def karritora_gehitu(request):
    product_id = request.POST['product_id']
    produktua = Produktua.objects.get(id=product_id)
    user = request.user
    bezeroa = Bezeroa.objects.get(user=user)
    karrito = Karrito.objects.filter(bezeroa=bezeroa).first()

    ##Karritorik ez badago sortu
    if karrito is None:
            karrito_berria = Karrito()
            karrito_berria.bezeroa = bezeroa
            karrito_berria.save()
            print("Karrito berria sortu da produktuarekin")

    ##Gehitu beharreko produktua aurkitu
    existing_item = KarritoItem.objects.filter(produktua=produktua,karrito=karrito).first()
    ##Produktua karritoan badago unitate bat gehiago gehitu
    if existing_item:
        existing_item.unitateak += 1
        existing_item.save()
    else:
        item = KarritoItem(produktua=produktua, unitateak=1,karrito=karrito)
        item.save()
        item.karrito = karrito

    return JsonResponse({'success': True})

@login_required
def karritotik_kendu(request):
    product_id = request.POST['product_id']
    produktua = Produktua.objects.get(id=product_id)
    user = request.user
    bezeroa = Bezeroa.objects.get(user=user)
    karrito = Karrito.objects.filter(bezeroa=bezeroa).first()

    ##Gehitu beharreko produktua aurkitu
    existing_item = KarritoItem.objects.filter(produktua=produktua,karrito=karrito).first()
    ##Produktua karritoan badago unitate bat gehiago gehitu
    if existing_item and existing_item.unitateak > 0:
        existing_item.unitateak -= 1
        existing_item.save()

    return JsonResponse({'success': True})

@login_required
def karritotik_ezabatu(request):
    user = request.user
    bezeroa = Bezeroa.objects.get(user=user)
    karrito = Karrito.objects.filter(bezeroa=bezeroa).first()
    item_id = request.POST['item_id']
    ##Sortutako itema ezabatu
    item = KarritoItem.objects.get(id=item_id,karrito=karrito)
    item.delete()


    return JsonResponse({'success': True})

def karritoko_unitateak(request):
    user = request.user
    bezeroa = Bezeroa.objects.get(user=user)
    karrito = Karrito.objects.filter(bezeroa=bezeroa).first()

    unitateak = KarritoItem.objects.count()

    return JsonResponse({'cart_count': unitateak})

@login_required
def erosketa_egin(request):
    user = request.user
    bez = Bezeroa.objects.get(user=user)
    
    karrito = Karrito.objects.filter(bezeroa=bez).first()

    ##PRODUKTUAK GORDETZEKO
    guz = 0
    produktuak = []
    items = KarritoItem.objects.filter(karrito=karrito)
    for i in items:
        produktua = i.produktua
        produktuak.append(produktua)
        guz = guz + (i.unitateak * i.produktua.prezioa) 
    
    erosketa = Erosketa()
    erosketa.bezeroa = bez
    erosketa.guztira = guz
    erosketa.save()  # Save the Erosketa object before setting the many-to-many relationship

    # Now, set the many-to-many relationship
    erosketa.produktuak.set(produktuak)

    ##Karritoa eta itemak ezabatu
    karrito.delete()
    items.delete()
    return HttpResponseRedirect(reverse('home'))

def gomendioak(request):
    produktuak = list(Produktua.objects.all())
    random_produktuak = random.sample(produktuak,10)

    data = [{"name": produktua.izena, "image": produktua.img.url} for produktua in random_produktuak]
    return JsonResponse(data, safe=False)




    