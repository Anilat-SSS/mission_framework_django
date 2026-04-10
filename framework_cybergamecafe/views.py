from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from .forms import SignUpForm
from .models import Reservation, Tournoi


# 🔐 Vérif admin
def is_admin(user):
    return user.is_staff


# =========================
# INSCRIPTION
# =========================
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('reservation')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})


# =========================
# CONNEXION
# =========================
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            return redirect('reservation')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


# =========================
# DECONNEXION
# =========================
def logout_view(request):
    logout(request)
    return redirect('login')


# =========================
# RESERVATION
# =========================
@login_required
def reservation(request):
    if request.method == "POST":
        motif = request.POST.get("motif")
        temps = request.POST.get("temps_secondes")
        tournoi_id = request.POST.get("tournoi")

        tournoi = None
        if tournoi_id:
            tournoi = get_object_or_404(Tournoi, id=tournoi_id)

        reservation = Reservation.objects.create(
            user=request.user,
            motif=motif,
            temps_secondes=temps,
            tournoi=tournoi
        )

        # 🔥 BONUS : ajoute automatiquement le participant au tournoi
        if tournoi:
            tournoi.participants.add(request.user)

        return redirect("reservation")

    tournois = Tournoi.objects.all()
    return render(request, "reservation.html", {"tournois": tournois})


# =========================
# TABLE USERS (ADMIN)
# =========================
@user_passes_test(is_admin)
def users_table_view(request):
    users = User.objects.all()
    return render(request, 'users_table.html', {'users': users})


# =========================
# GESTION TOURNOIS (CRUD)
# =========================
@login_required
@user_passes_test(is_admin)
def gestion_tournois(request):

    if request.method == "POST":
        nom = request.POST.get("nom")
        jeu = request.POST.get("jeu")
        date = request.POST.get("date")
        heure = request.POST.get("heure")

        if nom and jeu and date and heure:
            Tournoi.objects.create(
                nom=nom,
                jeu=jeu,
                date=date,
                heure=heure
            )

        return redirect("gestion_tournois")

    # 🔥 IMPORTANT : récupère TOUS les tournois
    tournois = Tournoi.objects.all().order_by("-date")

    return render(request, "gestion_tournois.html", {
        "tournois": tournois
    })


# =========================
# SUPPRIMER TOURNOI
# =========================
@login_required
@user_passes_test(is_admin)
def supprimer_tournoi(request, id):
    tournoi = get_object_or_404(Tournoi, id=id)

    if request.method == "POST":
        tournoi.delete()

    return redirect("gestion_tournois")

# =========================
# MODIFIER TOURNOI
# =========================
@login_required
@user_passes_test(is_admin)
def modifier_tournoi(request, id):
    tournoi = get_object_or_404(Tournoi, id=id)

    if request.method == "POST":
        tournoi.nom = request.POST.get("nom")
        tournoi.jeu = request.POST.get("jeu")
        tournoi.date = request.POST.get("date")
        tournoi.heure = request.POST.get("heure")
        tournoi.save()

        return redirect("gestion_tournois")

    return render(request, "modifier_tournoi.html", {
        "tournoi": tournoi
    })