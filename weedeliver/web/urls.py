from django.urls import path

from web import views

urlpatterns = [
    path('', views.index, name='index'),
    path('produktuak/', views.produktuak, name='produktuak'),
    path('produktua/<int:pid>/', views.produktua, name='produktua'),
    # path('produktua/<int:id>/karritora/', views.karritoa_gehitu, name='karritoa_gehitu'),
    path('kontaktua/', views.kontaktua, name='kontaktua'),
    # path('kontaktua/submit/', views.kontaktua_submit, name='kontaktua_submit'),
    # path('kontaktua/bidalita/', views.kontaktua_bidalita, name='kontaktua_bidalita'),
    # path('karritoa/', views.karritoa, name='karritoa'),
    path('signup/', views.signup_view, name='signup'),
    path('signup/kontuaSortu/', views.kontua_sortu, name='kontuaSortu'),
    path('login/', views.login_view, name='login'),
    path('login/auth/', views.auth, name='auth'),
    path('logout/', views.logout_view, name='logout'),
    path('kontua/', views.kontua, name='kontua'),
    path('kontua/aldatu/', views.kontua_aldatu, name='kontua_aldatu'),
    path('kontua/aldatu/gorde/', views.kontua_aldaketak_gorde, name='kontua_aldaketak_gorde'),
    path('harpidetu/', views.plus, name='plus'),
    path('harpidetza/erosi/', views.harpidetu, name='minus'),
]
