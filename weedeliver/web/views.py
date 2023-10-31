from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Bezeroa,Kategoria,Produktua,Deskontua,Erosketa

# Create your views here.
def home(request):
    return render(request,'home.html')

def kontaktua(request):
    return render(request,'kontaktua.html')

def produktuak(request):
    produktuak = Produktua.objects.all()
    kategoriak = Kategoria.objects.all()
    return render(request,'produktuak.html',{"produktuak":produktuak,"kategoriak":kategoriak})