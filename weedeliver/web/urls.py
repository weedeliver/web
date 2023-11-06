from . import views
from django.urls import path

urlpatterns = [
    path('', views.home,name='home'),
    path('kontaktua/',views.kontaktua,name="kontaktua"),
    path('produktuak/',views.produktuak,name="produktuak"),
    path('produktuak/karritora_gehitu/',views.karritora_gehitu,name="karritora_gehitu"),
    path('login/',views.login_view,name="login"),
    path('login/saioa_hasi/',views.saioa_hasi,name="saioa_hasi"),
    path('signup/',views.signup,name="signup"),
    path('signup/kontuaSortu/',views.kontua_sortu,name="kontuaSortu"),
    path('profila/',views.profila,name="profila"),
    path('profila/logout/',views.saioa_itxi,name="logout"),
    path('karrito/',views.karrito_view,name="karrito"),
    path('karrito/karritotik_ezabatu/',views.karritotik_ezabatu,name="karritotik_ezabatu")
]