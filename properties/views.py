from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import Property
from .forms import PropertyForm


def staff_required(view_func):
    @wraps(view_func)
    @login_required(login_url="login")
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden(
                "You are not allowed to manage properties."
            )

        return view_func(request, *args, **kwargs)

    return wrapper


# Public website: show all properties
def property_list(request):
    properties = Property.objects.all()

    return render(
        request,
        "properties/property_list.html",
        {"properties": properties},
    )


# Admin dashboard
@staff_required
def property_dashboard(request):
    properties = Property.objects.all()

    return render(
        request,
        "properties/property_dashboard.html",
        {"properties": properties},
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

        messages.success(
            request,
            "Property added successfully!",
        )

        return redirect("property_dashboard")

    return render(
        request,
        "properties/property_form.html",
        {
            "form": form,
            "page_title": "Add Property",
        },
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

        messages.success(
            request,
            "Property updated successfully!",
        )

        return redirect("property_dashboard")

    return render(
        request,
        "properties/property_form.html",
        {
            "form": form,
            "page_title": "Edit Property",
        },
    )


# Delete property and its uploaded image
@staff_required
@require_POST
def property_delete(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)

    if property_obj.image:
        property_obj.image.delete(save=False)

    property_obj.delete()

    messages.success(
        request,
        "Property deleted successfully!",
    )

    return redirect("property_dashboard")