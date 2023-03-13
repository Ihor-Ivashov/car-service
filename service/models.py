from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import UniqueConstraint


class Car(models.Model):
    model = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=10)
    VIN = models.CharField(max_length=17)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["VIN"], name="unique_VIN"),
            UniqueConstraint(
                fields=["registration_number"],
                name="unique_registration_number"
            )
        ]

    def __str__(self):
        return f"{self.model} - {self.registration_number}"


class Customer(AbstractUser):
    cars = models.ManyToManyField(Car, related_name="cars")

    class Meta:
        verbose_name = "customer"
        verbose_name_plural = "customers"

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class Part(models.Model):
    name = models.CharField(max_length=255)
    measure = models.CharField(max_length=15)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["name"], name="unique_name")
        ]
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.measure})"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    car = models.ForeignKey(Car, on_delete=models.PROTECT)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"#{self.id} - {self.created_at}"


class OrderRow(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    part = models.ForeignKey(Part, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=8, decimal_places=3)
    sum = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.part} - {self.quantity} = {self.sum}"
