from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('', views.accueil, name='accueil'),  # page d'accueil
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('tournois/', views.gestion_tournois, name='gestion_tournois'),
    path('tournoi/modifier/<int:id>/', views.modifier_tournoi, name='modifier_tournoi'),
    path('tournoi/supprimer/<int:id>/', views.supprimer_tournoi, name='supprimer_tournoi'),
]