from . import views
from django.urls import path

urlpatterns = [
    path('', views.home,name='home'),
    path('kontaktua/',views.kontaktua,name="kontaktua"),
    path('produktuak/',views.produktuak,name="produktuak")
]