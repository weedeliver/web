from django.urls import path

from web import views

urlpatterns = [
    path('', views.index, name='index'),
    path('produktuak/', views.produktuak, name='produktuak'),
    path('produktuak/<str:cat>/', views.produktuak_kategoria, name='produktuak_kategoria'),
    path('produktua/<int:pid>/', views.produktua, name='produktua'),
    path('produktua/<int:pid>/gehitu/', views.saskira_gehitu, name='saskira_gehitu'),
    path('unitateak_aldatu/',views.unitateak_aldatu,name="unitateak_aldatu"),
    path('kontaktua/', views.kontaktua, name='kontaktua'),
    # path('kontaktua/submit/', views.kontaktua_submit, name='kontaktua_submit'),
    # path('kontaktua/bidalita/', views.kontaktua_bidalita, name='kontaktua_bidalita'),
    path('saskia/', views.saskia_view, name='saskia'),
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
