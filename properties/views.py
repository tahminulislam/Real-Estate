
from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Property, FeaturedOffer
from .forms import PropertyForm, FeaturedOfferForm


def staff_required(view_func):
    @wraps(view_func)
    @login_required(login_url="login")
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden(
                "You are not allowed to manage this page."
            )
        return view_func(request, *args, **kwargs)
    return wrapper


def active_offers():
    now = timezone.now()
    return FeaturedOffer.objects.filter(
        is_active=True,
        starts_at__lte=now,
        expires_at__gt=now,
    ).order_by("-starts_at")


# Public property listing
def property_list(request):
    properties = Property.objects.all()
    offers = active_offers()

    return render(
        request,
        "properties/property_list.html",
        {"properties": properties, "offers": offers},
    )


# Staff dashboard
@staff_required
def property_dashboard(request):
    properties = Property.objects.all()
    offers = FeaturedOffer.objects.all().order_by("-starts_at")

    return render(
        request,
        "properties/property_dashboard.html",
        {"properties": properties, "offers": offers},
    )


# Add property
@staff_required
def property_add(request):
    form = PropertyForm(
        request.POST or None,
        request.FILES or None,
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Property added successfully!")
        return redirect("property_dashboard")

    return render(
        request,
        "properties/property_form.html",
        {"form": form, "page_title": "Add Property"},
    )


# Edit property
@staff_required
def property_edit(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    form = PropertyForm(
        request.POST or None,
        request.FILES or None,
        instance=property_obj,
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Property updated successfully!")
        return redirect("property_dashboard")

    return render(
        request,
        "properties/property_form.html",
        {"form": form, "page_title": "Edit Property"},
    )


# Delete property
@staff_required
@require_POST
def property_delete(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)

    if property_obj.image:
        property_obj.image.delete(save=False)

    property_obj.delete()
    messages.success(request, "Property deleted successfully!")
    return redirect("property_dashboard")


# Add featured offer
@staff_required
def offer_add(request):
    form = FeaturedOfferForm(
        request.POST or None,
        request.FILES or None,
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Featured offer added successfully!")
        return redirect("property_dashboard")

    return render(
        request,
        "properties/offer_form.html",
        {"form": form, "page_title": "Add Featured Offer"},
    )


# Edit featured offer
@staff_required
def offer_edit(request, pk):
    offer = get_object_or_404(FeaturedOffer, pk=pk)
    form = FeaturedOfferForm(
        request.POST or None,
        request.FILES or None,
        instance=offer,
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Featured offer updated successfully!")
        return redirect("property_dashboard")

    return render(
        request,
        "properties/offer_form.html",
        {"form": form, "page_title": "Edit Featured Offer"},
    )


# Delete featured offer
@staff_required
@require_POST
def offer_delete(request, pk):
    offer = get_object_or_404(FeaturedOffer, pk=pk)

    if offer.image:
        offer.image.delete(save=False)

    offer.delete()
    messages.success(request, "Featured offer deleted successfully!")
    return redirect("property_dashboard")


# Public offer details
def offer_detail(request, pk):
    offer = get_object_or_404(FeaturedOffer, pk=pk)
    return render(
        request,
        "properties/offer_detail.html",
        {"offer": offer},
    )
