from django.shortcuts import render

from web.models import Produktua, Kategoria


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
    return render(request, 'produktua.html', {'produktua': produktua})


def kontaktua(request):
    return render(request, 'kontaktua.html')