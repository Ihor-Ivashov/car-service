from django.urls import path

from service.views import (
    index, CarListView, CarDetailView, CarCreateView, CarUpdateView,
    CarDeleteView, PartListView, PartDetailView, PartCreateView,
    PartUpdateView, PartDeleteView, CustomerListView, CustomerDetailView,
    CustomerCreateView, CustomerUpdateView, CustomerDeleteView
)


urlpatterns = [
    path("", index, name="index"),
    path("cars/", CarListView.as_view(), name="car-list"),
    path("cars/<int:pk>/", CarDetailView.as_view(), name="car-detail"),
    path("cars/create", CarCreateView.as_view(), name="car-create"),
    path("cars/<int:pk>/update/", CarUpdateView.as_view(), name="car-update"),
    path("cars/<int:pk>/delete/", CarDeleteView.as_view(), name="car-delete"),
    path("parts/", PartListView.as_view(), name="part-list"),
    path("parts/<int:pk>/", PartDetailView.as_view(), name="part-detail"),
    path("parts/create", PartCreateView.as_view(), name="part-create"),
    path(
        "parts/<int:pk>/update/",
        PartUpdateView.as_view(),
        name="part-update"
    ),
    path(
        "parts/<int:pk>/delete/",
        PartDeleteView.as_view(),
        name="part-delete"
    ),
    path("customers/", CustomerListView.as_view(), name="customer-list"),
    path(
        "customers/<int:pk>/",
        CustomerDetailView.as_view(),
        name="customer-detail"
    ),
    path(
        "customers/create/",
        CustomerCreateView.as_view(),
        name="customer-create"
    ),
    path(
        "customers/<int:pk>/update/",
        CustomerUpdateView.as_view(),
        name="customer-update"
    ),
    path(
        "customers/<int:pk>/delete/",
        CustomerDeleteView.as_view(),
        name="customer-delete"
    ),
]

app_name = "service"
