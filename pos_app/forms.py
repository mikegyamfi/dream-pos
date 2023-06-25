from django import forms
from django.contrib.auth.forms import UserCreationForm

from pos_app import models
from . import helper


class CustomUserForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(
        {'class': 'form-control form-control-lg', 'autocomplete': 'off', 'placeholder': 'First Name'}))
    last_name = forms.CharField(
        widget=forms.TextInput(
            {'class': 'form-control form-control-lg', 'autocomplete': 'off', 'placeholder': 'Last Name'}))
    username = forms.CharField(
        widget=forms.TextInput(
            {'class': 'form-control form-control-lg', 'autocomplete': 'off', 'placeholder': 'Username'}))
    email = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Email'}))
    phone_number = forms.CharField(
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Phone Number'}))
    role = forms.ChoiceField(widget=forms.Select({'class': 'form-control form-control-lg', 'placeholder': 'Role'}),
                             choices=(('Admin', 'Admin'), ('Sales Personnel', 'Sales Personnel')))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Password'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = models.CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'role', 'password1', 'password2']


class AddProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=None, to_field_name='name', empty_label=None,
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 0.1}))
    # size = forms.ModelChoiceField(queryset=None, to_field_name='name', empty_label=None,
    #                               widget=forms.Select(attrs={'class': 'form-control'}))
    size = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=(
        ("S/S", "S/S"), ("Q/S", "Q/S"), ("M/S", "M/S"), ("A/S", "A/S"), ("B/S", "B/S"), ("E/L", "E/L")))
    quantity = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

    def __init__(self, domain, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = models.Category.objects.filter(domain=domain)
        # self.fields['size'].queryset = models.Size.objects.filter(domain=domain)

    class Meta:
        model = models.Product
        fields = ['category', 'name', 'price', 'quantity']


class EditProductForm(forms.Form):
    price = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 0.1}))
    quantity = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    category = forms.ModelChoiceField(queryset=None, to_field_name='name', empty_label=None,
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    size = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=(
        ("S/S", "S/S"), ("Q/S", "Q/S"), ("M/S", "M/S"), ("A/S", "A/S"), ("B/S", "B/S"), ("E/L", "E/L")))
    # size = forms.ModelChoiceField(queryset=None, to_field_name='name', empty_label=None,
    #                               widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, domain, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = models.Category.objects.filter(domain=domain)
        # self.fields['size'].queryset = models.Size.objects.filter(domain=domain)


class RestockProductForm(forms.Form):
    category = forms.ModelChoiceField(queryset=None, to_field_name='name', empty_label=None,
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 0.1}))
    quantity = forms.CharField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'aria-describedby': 'basic-addon1'}))
    size = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=(
        ("S/S", "S/S"), ("Q/S", "Q/S"), ("M/S", "M/S"), ("A/S", "A/S"), ("B/S", "B/S"), ("E/L", "E/L")))
    # size = forms.ModelChoiceField(queryset=None, to_field_name='name', empty_label=None,
    #                               widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, domain, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = models.Category.objects.filter(domain=domain)
        # self.fields['size'].queryset = models.Size.objects.filter(domain=domain)


class AddCategoryForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = models.Category
        fields = ['name', 'description']



