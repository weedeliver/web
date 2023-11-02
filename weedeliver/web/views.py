from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from web.models import Produktua, Kategoria, Bezeroa


# Create your views here.
def index(request):
    return render(request, 'index.html')


def produktuak(request):
    produktuak = Produktua.objects.all()
    kategoriak = Kategoria.objects.all()
    return render(request, 'produktuak.html', {'produktuak': produktuak, 'kategoriak': kategoriak})


def produktuak_kategoria(request, cat):
    produktuak = Produktua.objects.filter(izena=cat)
    kategoriak = Kategoria.objects.all()
    aukeratutako_kategoria = Kategoria.objects.get(izena=cat)
    return render(request, 'produktuak.html', {'produktuak': produktuak, 'kategoriak': kategoriak, 'aukeratutako_kategoria': aukeratutako_kategoria})


def produktua(request, pid):
    produktua = Produktua.objects.get(id=pid)
    kategoriak = Produktua.objects.filter(id=pid).values('kategoria__izena')
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
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Log the user in
            user = form.get_user()
            login(request, user)  # Pass the request and user to login
            return HttpResponseRedirect(reverse('index'))
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})


def logout_view(request):
    # log out the user and redirect to the index page
    logout(request)
    return HttpResponseRedirect(reverse('index'))
