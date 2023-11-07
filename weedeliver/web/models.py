from django.conf import settings
from django.db import models


# Create your models here.
class Bezeroa(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    izena = models.CharField(max_length=100)
    abizena = models.CharField(max_length=100)
    emaila = models.CharField(max_length=100)
    telefonoa = models.IntegerField()
    helbidea = models.TextField(null=True)
    herria = models.CharField(max_length=100, null=True)
    posta_kodea = models.IntegerField(null=True)
    txartela = models.IntegerField(null=True)
    harpidetza = models.CharField(max_length=50)

    def __str__(self):
        return self.izena + " " + self.abizena


class Kategoria(models.Model):
    izena = models.CharField(max_length=100)

    def __str__(self):
        return self.izena


class Deskontua(models.Model):
    izena = models.CharField(max_length=100)
    kantitatea = models.IntegerField()
    isEhunekoa = models.BooleanField()

    def __str__(self):
        return self.izena


class Produktua(models.Model):
    izena = models.CharField(max_length=100)
    deskribapena = models.TextField()
    kategoria = models.ManyToManyField(Kategoria)
    prezioa = models.FloatField()
    deskontua = models.ForeignKey(Deskontua,on_delete=models.CASCADE)
    img = models.ImageField(upload_to='web/static/irudiak/produktuak/')

    def __str__(self):
        return self.izena


class Erosketa(models.Model):
    bezeroa = models.ForeignKey(Bezeroa,on_delete=models.CASCADE)
    produktuak = models.ManyToManyField(Produktua)
    data = models.DateTimeField(auto_now_add=True)
    totala = models.FloatField()


class Saskia_item(models.Model):
    produktua = models.ForeignKey(Produktua,on_delete=models.CASCADE)
    kantitatea = models.IntegerField()


class Saskia(models.Model):
    bezeroa = models.ForeignKey(Bezeroa,on_delete=models.CASCADE)
    saskia_items = models.ManyToManyField(Saskia_item)
