from django.shortcuts import render

from service.models import Customer, Car, Order


def index(request):
    num_customers = Customer.objects.count()
    num_cars = Car.objects.count()
    num_orders = Order.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_customers": num_customers,
        "num_cars": num_cars,
        "num_orders": num_orders,
        "num_visits": num_visits + 1,
    }

    return render(request, "service/index.html", context=context)
