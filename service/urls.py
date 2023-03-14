from django.urls import path

from service.views import index, CarListView, CarDetailView

urlpatterns = [
    path("", index, name="index"),
    path("cars/", CarListView.as_view(), name="car-list"),
    path("cars/<int:pk>/", CarDetailView.as_view(), name="car-detail"),
]

app_name = "service"
