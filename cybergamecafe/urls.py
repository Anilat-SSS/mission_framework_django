"""
URL configuration for cybergamecafe project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from framework_cybergamecafe import views  

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('reservation/', views.reservation, name='reservation'),
    path('logout/', views.logout_view, name='logout_view'),

    # 🔥 TOURNOIS
    path('tournois/', views.gestion_tournois, name='gestion_tournois'),
    path('tournoi/modifier/<int:id>/', views.modifier_tournoi, name='modifier_tournoi'),
    path('tournoi/supprimer/<int:id>/', views.supprimer_tournoi, name='supprimer_tournoi'),
]