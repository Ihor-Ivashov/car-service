from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from django import forms
from django.db.models import Q

from service.models import Car


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


class CustomerForm(UserCreationForm):
    cars = forms.ModelMultipleChoiceField(
        queryset=Car.objects.filter(customers=None),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "cars",
        )

    def save(self, commit=True):
        user = super(CustomerForm, self).save()
        user.cars.set(self.cleaned_data.get("cars"))
        user.save()
        return user


class CustomerUpdateForm(forms.ModelForm):
    cars = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def __init__(self, pk,  *args, **kwargs):
        super(CustomerUpdateForm, self).__init__(*args, **kwargs)
        self.fields["cars"].queryset = Car.objects.filter(
            Q(customers=None) | Q(customers__id=pk)
        )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "cars",
        )


class CarsSearchForm(forms.Form):
    search_string = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by model, reg. number, VIN...",
                   "size": 50,
                   "class": "form-control"}
        )
    )


class PartsCustomersSearchForm(forms.Form):
    search_string = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by name...",
                   "size": 50,
                   "class": "form-control"}
        )
    )


class OrdersSearchForm(forms.Form):
    search_string = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by customer name | car reg. number...",
                "size": 50,
                "class": "form-control"
            }
        )
    )
