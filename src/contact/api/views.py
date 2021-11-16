from rest_framework import generics


from contact.models import Contact
from .serializers import ContactSerializer

class ContactCreateAPIView(generics.CreateAPIView):
    print("contact api processed")
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = []
    authentication_classes = []
