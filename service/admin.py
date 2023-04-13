from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import Customer, Car, Part, Order


@admin.register(Customer)
class CustomerAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("cars",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "cars",
                    )
                },
            ),
        )
    )


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    search_fields = ("model", "VIN", "registration_number")


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    search_fields = ("name", )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    search_fields = ("id", )


admin.site.unregister(Group)
