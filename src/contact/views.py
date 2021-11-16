from django.shortcuts import render
from django.http import JsonResponse

from .models import Contact
from .forms import ContactForm

# Create your views here.

def contact_page(request):
    form = ContactForm(request.POST or None)
    template = "contact/modal.html"
    contact_added = False

    if request.is_ajax():
        if form.is_valid():
            fullname = form.cleaned_data.get("fullname")
            email = form.cleaned_data.get("email")
            message = form.cleaned_data.get("message")

            obj = Contact()
            obj.fullname = fullname
            obj.email = email
            obj.message = message
            obj.save()
            contact_added = True

        error =  form.errors
        data = {
            "added": contact_added,
            "statusError": error
        }
        return JsonResponse(data, status_code=400)

        # if not form.is_valid():
        #     formError =  form.errors
        #     data = {
        #         "errors": formError
        #     }
        #     return JsonResponse(data)
        # send_mail(
        #     'Contact Us',
        #     message,
        #     email,
        #     ['caesar.orz@gmail.com'],
        #     fail_silently=False,
        # )

    context = {
        "form": form
    }
    return render(request, template, context)
