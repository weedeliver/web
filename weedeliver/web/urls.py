from django.urls import path

from web import views

urlpatterns = [
    path('', views.index, name='index'),
    path('produktuak/', views.produktuak, name='produktuak'),
    # path('produktua/<int:id>', views.produktua, name='produktua'),
    # path('produktua/<int:id>/gehitu/', views.karritoa_gehitu, name='karritoa_gehitu'),
    path('kontaktua/', views.kontaktua, name='kontaktua'),
    # path('kontaktua/submit/', views.kontaktua_submit, name='kontaktua_submit'),
    # path('kontaktua/bidalita/', views.kontaktua_bidalita, name='kontaktua_bidalita'),
    # path('karritoa/', views.karritoa, name='karritoa'),
]
