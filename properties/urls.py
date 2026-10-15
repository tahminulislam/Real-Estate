
from django.urls import path
from . import views

urlpatterns = [
    path("", views.property_list, name="property_list"),

    path("manage/", views.property_dashboard, name="property_dashboard"),
    path("manage/add/", views.property_add, name="property_add"),
    path("manage/edit/<int:pk>/", views.property_edit, name="property_edit"),
    path("manage/delete/<int:pk>/", views.property_delete, name="property_delete"),

    path("manage/offers/add/", views.offer_add, name="offer_add"),
    path("manage/offers/edit/<int:pk>/", views.offer_edit, name="offer_edit"),
    path("manage/offers/delete/<int:pk>/", views.offer_delete, name="offer_delete"),

    path("offers/<int:pk>/", views.offer_detail, name="offer_detail"),
]
