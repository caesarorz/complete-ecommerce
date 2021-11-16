from django import forms
from .models import Address


class AddressForm(forms.ModelForm):

    direccion_linea_1 = forms.CharField(label='', required='False', widget=forms.TextInput(attrs={"class": 'form-control my-1', 'placeholder': 'Dirección 1'}))
    direccion_linea_2 = forms.CharField(label='', required='False', widget=forms.TextInput(attrs={"class": 'form-control my-1', 'placeholder': 'Dirección 2'}))
    # pais = forms.CharField(label='', widget=forms.TextInput(attrs={"class": 'form-control my-1', 'placeholder': 'Costa Rica'}))
    provincia = forms.CharField(label='', required='False', widget=forms.TextInput(attrs={"class": 'form-control my-1', 'placeholder': 'Provincia'}))
    canton = forms.CharField(label='', required='False', widget=forms.TextInput(attrs={"class": 'form-control my-1', 'placeholder': 'Cantón'}))
    distrito = forms.CharField(label='', required='False', widget=forms.TextInput(attrs={"class": 'form-control my-1', 'placeholder': 'Distrito'}))
    class Meta:
        model = Address
        fields = [
            #'billing_profile',
            #'address_type',
            'direccion_linea_1',
            'direccion_linea_2',
            # 'pais',
            'provincia',
            'canton',
            'distrito',
            # 'codigo_postal',
        ]
