from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, QuerySet
from django.http import HttpResponseRedirect, HttpResponseBadRequest, \
    JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic

from service.forms import (CustomerForm, CustomerUpdateForm, CarsSearchForm,
                           PartsCustomersSearchForm, OrdersSearchForm)
from service.models import (Customer, Car, Order, Part, OrderRow)


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

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super(CarListView, self).get_context_data(**kwargs)
        search_string = self.request.GET.get("search_string")
        context["search_form"] = CarsSearchForm(
            initial={"search_string": search_string}
        )
        return context

    def get_queryset(self) -> QuerySet:
        queryset = Car.objects.all().prefetch_related("customers")
        search_string = self.request.GET.get("search_string", "")
        if search_string:
            return queryset.filter(
                Q(model__icontains=search_string)
                | Q(registration_number__icontains=search_string)
                | Q(VIN__icontains=search_string)
            )
        return queryset


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

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super(PartListView, self).get_context_data(**kwargs)
        search_string = self.request.GET.get("search_string")
        context["search_form"] = PartsCustomersSearchForm(
            initial={"search_string": search_string}
        )
        return context

    def get_queryset(self) -> QuerySet:
        queryset = Part.objects.all()
        search_string = self.request.GET.get("search_string", "")
        if search_string:
            return queryset.filter(name__icontains=search_string)
        return queryset


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

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super(CustomerListView, self).get_context_data(**kwargs)
        search_string = self.request.GET.get("search_string")
        context["search_form"] = PartsCustomersSearchForm(
            initial={"search_string": search_string}
        )
        return context

    def get_queryset(self) -> QuerySet:
        queryset = Customer.objects.all()
        search_string = self.request.GET.get("search_string", "")
        if search_string:
            return queryset.filter(
                Q(username__icontains=search_string)
                | Q(first_name__icontains=search_string)
                | Q(last_name__icontains=search_string)
            )
        return queryset


class CustomerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Customer


class CustomerCreateView(LoginRequiredMixin, generic.CreateView):
    model = get_user_model()
    form_class = CustomerForm


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


class OrderListView(LoginRequiredMixin, generic.ListView):
    model = Order

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super(OrderListView, self).get_context_data(**kwargs)
        search_string = self.request.GET.get("search_string")
        context["search_form"] = OrdersSearchForm(
            initial={"search_string": search_string}
        )
        return context

    def get_queryset(self) -> QuerySet:
        queryset = Order.objects.all().select_related("customer", "car")
        search_string = self.request.GET.get("search_string", "")
        if search_string:
            return queryset.filter(
                Q(customer__username__icontains=search_string)
                | Q(customer__first_name__icontains=search_string)
                | Q(customer__last_name__icontains=search_string)
                | Q(car__registration_number__icontains=search_string)
            )
        return queryset


class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    model = Order


class OrderCreateView(LoginRequiredMixin, generic.CreateView):
    model = Order
    fields = "__all__"
    success_url = reverse_lazy("service:order-list")


class OrderUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Order
    fields = "__all__"
    success_url = reverse_lazy("service:order-list")


class OrderDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Order
    success_url = reverse_lazy("service:order-list")


class OrderRowCreateView(LoginRequiredMixin, generic.CreateView):
    model = OrderRow
    fields = "__all__"
    template_name = "service/order_row_form.html"

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super(OrderRowCreateView, self).get_context_data(**kwargs)
        context["order"] = Order.objects.get(pk=self.kwargs["pk"])
        return context

    def get_initial(self):
        return {"order": self.kwargs["pk"]}


def order_row_delete(request, pk):
    row = OrderRow.objects.get(pk=pk)
    order_id = row.order_id
    row.delete()
    return HttpResponseRedirect(
        reverse("service:order-detail", kwargs={"pk": order_id})
    )


def get_customer_cars(request):
    if request.method == 'POST':
        customer_id = request.POST.get("customer_field")
        # field1_value = some_function(field2_value)

        cars = []
        queryset = Car.objects.filter(customers__id=int(customer_id))
        for car in queryset:
            cars.append({
                "id": car.id,
                "name": car.model
            })

        response_data = {"cars": cars}
        return JsonResponse(response_data)
    else:
        return HttpResponseBadRequest()
