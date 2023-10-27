from django.db import models

# Create your models here.
class Bezeroa(models.Model):
    izena = models.CharField(max_length=100)
    abizena = models.CharField(max_length=100)
    emaila = models.CharField(max_length=100)
    telefonoa = models.IntegerField()
    helbidea = models.TextField()
    txartela = models.IntegerField()
    harpidetza = models.CharField(max_length=50)


class Kategoria(models.Model):
    izena = models.CharField(max_length=100)

class Deskontua(models.Model):
    izena = models.CharField(max_length=100)
    kantitatea = models.IntegerField()
    isEhunekoa = models.BooleanField()

class Produktua(models.Model):
    izena = models.CharField(max_length=100)
    deskribapena = models.TextField()
    kategoria = models.ManyToManyField(Kategoria)
    prezioa = models.FloatField()
    deskontua = models.ForeignKey(Deskontua,on_delete=models.CASCADE)

class Erosketa(models.Model):
    bezeroa = models.ForeignKey(Bezeroa,on_delete=models.CASCADE)
    produktuak = models.ManyToManyField(Produktua)
    data = models.DateTimeField(auto_now_add=True)