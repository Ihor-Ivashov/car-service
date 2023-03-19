from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from django import forms
from django.db.models import Count, Q

from service.models import Car, Customer


class CustomerForm(UserCreationForm):
    cars = forms.ModelMultipleChoiceField(
        queryset=Car.objects.filter(customers=None),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "cars",
        )

    def save(self, commit=True):
        user = super(CustomerForm, self).save(commit=False)
        user.cars.set(self.cleaned_data.get("cars"))
        user.save()
        return user


class CustomerUpdateForm(forms.ModelForm):
    cars = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, pk,  *args, **kwargs):
        super(CustomerUpdateForm, self).__init__(*args, **kwargs)
        self.fields.get("cars").queryset = Car.objects.filter(
            Q(customers=None) | Q(customers__id=pk)
        )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "cars",
        )
