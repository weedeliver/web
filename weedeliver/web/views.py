from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import Bezeroa,Kategoria,Produktua,Deskontua,Erosketa,Karrito,KarritoItem

# Create your views here.
def home(request):
    return render(request,'home.html')

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
    return render(request,'profila.html',{"bezeroa": bezeroa})


@login_required
def saioa_itxi(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def karrito_view(request):
    user = request.user
    bezeroa = Bezeroa.objects.get(user=user)
    karrito = Karrito.objects.filter(bezeroa=bezeroa).first()
    return render(request,'karrito.html',{"karrito":karrito})

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
    existing_item = karrito.karrito_itemak.filter(produktua=produktua).first()
    ##Produktua karritoan badago unitate bat gehiago gehitu
    if existing_item:
        existing_item.unitateak += 1
        existing_item.save()
    else:
        item = KarritoItem(produktua=produktua, unitateak=1)
        item.save()
        karrito.karrito_itemak.add(item)

    return JsonResponse({'success': True})

@login_required
def karritotik_ezabatu(request):
    item_id = request.POST['item_id']
    ##Sortutako itema ezabatu
    item = KarritoItem.objects.get(id=item_id)
    item.delete()


    return JsonResponse({'success': True})

    