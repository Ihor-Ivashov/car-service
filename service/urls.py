from django.urls import path

from service.views import (
    index, CarListView, CarDetailView, CarCreateView, CarUpdateView,
    CarDeleteView
)

urlpatterns = [
    path("", index, name="index"),
    path("cars/", CarListView.as_view(), name="car-list"),
    path("cars/<int:pk>/", CarDetailView.as_view(), name="car-detail"),
    path("cars/create", CarCreateView.as_view(), name="car-create"),
    path("cars/<int:pk>/update/", CarUpdateView.as_view(), name="car-update"),
    path("cars/<int:pk>/delete/", CarDeleteView.as_view(), name="car-delete"),

]

app_name = "service"
