from rest_framework import serializers
from django import forms

from contact.models import Contact

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['fullname', 'email', 'message']

    def validate_email(self, value):
        email = value
        return email
