from django import forms
from django.core import validators
from .models import Contact


class ContactForm(forms.ModelForm):
    fullname = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Your name"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control", "placeholder": "Your email"}))
    message = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control", "placeholder": "Your Message"}))

    class Meta:
        model = Contact
        fields = ['fullname', 'email', 'message']

    def cleaned_data(self):
        email = self.cleaned_data.get("email")
        return email
