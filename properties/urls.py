from django.urls import path
from . import views

urlpatterns = [
    path(
        "",
        views.property_list,
        name="property_list",
    ),
    path(
        "manage/",
        views.property_dashboard,
        name="property_dashboard",
    ),
    path(
        "manage/add/",
        views.property_add,
        name="property_add",
    ),
    path(
        "manage/edit/<int:pk>/",
        views.property_edit,
        name="property_edit",
    ),
    path(
        "manage/delete/<int:pk>/",
        views.property_delete,
        name="property_delete",
    ),
]