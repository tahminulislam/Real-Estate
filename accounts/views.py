
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm
from properties.models import Property, FeaturedOffer
from django.utils import timezone

def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = RegistrationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("dashboard")

    return render(
        request,
        "accounts/register.html",
        {"form": form},
    )


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect("property_dashboard")
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:
            login(request, user)

            if user.is_staff:
                return redirect("property_dashboard")

            return redirect("dashboard")

        messages.error(request, "Invalid username or password.")

    return render(request, "accounts/login.html")



@login_required
def dashboard_view(request):
    properties = Property.objects.all()

    now = timezone.now()
    offers = FeaturedOffer.objects.filter(
        is_active=True,
        starts_at__lte=now,
        expires_at__gt=now,
    ).order_by("-starts_at")

    return render(
        request,
        "accounts/dashboard.html",
        {
            "properties": properties,
            "offers": offers,
        },
    )



@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")

    return redirect("dashboard")