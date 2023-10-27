from django.contrib import admin
from .models import Deskontua,Produktua,Erosketa,Bezeroa,Kategoria
# Register your models here.
class BezeroaAdmin(admin.ModelAdmin):
    list_display = ['izena','abizena','emaila','telefonoa','helbidea','txartela','harpidetza']
    list_filter = ['izena','abizena','emaila','telefonoa','helbidea','txartela','harpidetza']
    search_fields = ['izena','abizena','emaila','telefonoa','helbidea','txartela','harpidetza']

admin.site.register(Bezeroa,BezeroaAdmin)


class KategoriaAdmin(admin.ModelAdmin):
    list_display = ['izena']
    list_filter = ['izena']
    search_fields = ['izena']

admin.site.register(Kategoria,KategoriaAdmin)

class DeskontuaAdmin(admin.ModelAdmin):
    list_display = ['izena','kantitatea','isEhunekoa']
    list_filter = ['izena','kantitatea','isEhunekoa']
    search_fields = ['izena','kantitatea','isEhunekoa']

admin.site.register(Deskontua,DeskontuaAdmin)

class ProduktuaAdmin(admin.ModelAdmin):
    list_display = ['izena','deskribapena','prezioa','deskontua']
    list_filter = ['izena','deskribapena','prezioa','deskontua']
    search_fields = ['izena','deskribapena','prezioa','deskontua']

admin.site.register(Produktua,ProduktuaAdmin)

class ErosketaAdmin(admin.ModelAdmin):
    list_display = ['bezeroa','data']
    list_filter = ['bezeroa','data']
    search_fields = ['bezeroa','data']

admin.site.register(Erosketa,ErosketaAdmin)