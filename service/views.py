from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from service.forms import CustomerForm, CustomerUpdateForm
from service.models import Customer, Car, Order, Part


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


class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    paginate_by = 12
    queryset = Car.objects.all().prefetch_related("customers")


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car


class CarCreateView(LoginRequiredMixin, generic.CreateView):
    model = Car
    fields = "__all__"


class CarUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Car
    fields = "__all__"


class CarDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Car
    success_url = reverse_lazy("service:car-list")


class PartListView(LoginRequiredMixin, generic.ListView):
    model = Part
    paginate_by = 12


class PartDetailView(LoginRequiredMixin, generic.DetailView):
    model = Part


class PartCreateView(LoginRequiredMixin, generic.CreateView):
    model = Part
    fields = "__all__"
    success_url = reverse_lazy("service:part-list")


class PartUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Part
    fields = "__all__"
    success_url = reverse_lazy("service:part-list")


class PartDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Part
    success_url = reverse_lazy("service:part-list")


class CustomerListView(LoginRequiredMixin, generic.ListView):
    model = Customer
    paginate_by = 12


class CustomerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Customer


class CustomerCreateView(LoginRequiredMixin, generic.CreateView):
    model = get_user_model()
    form_class = CustomerForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cars_list"] = Car.objects.prefetch_related("customers").filter(customers=None)
        return context


class CustomerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    form_class = CustomerUpdateForm

    def get_form_kwargs(self):
        kwargs = super(CustomerUpdateView, self).get_form_kwargs()
        kwargs.update(self.kwargs)
        return kwargs


class CustomerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = get_user_model()
    success_url = reverse_lazy("service:customer-list")
