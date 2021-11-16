from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from django.views.generic import ListView
from django.db.models import Q

from .forms import ContactForm

# register forms and views
from accounts.forms import LoginForm, RegisterForm, LoginFormAlter

from catalog.models import Catalog, CatalogCategory
from products.models import Product
from carts.models import Cart, CartItem
from slideshow.models import Carousel, Slide

def home_page(request):

    home_slides = Slide.objects.filter(carousel__title="homepage")
    products = Product.objects.featured().order_by("?")
    categories = CatalogCategory.objects.all()

    login_form = LoginFormAlter
    register_form = RegisterForm

    cart_id = request.session.get("cart_id")
    cart = None
    cart_items = None

    if cart_id is not None:
        cart = Cart.objects.get(id=cart_id)
        cart_items = cart.cartitem_set.all()


    context =   {
            'home_slides': home_slides,
            'value': 'Categorias Productos',
            'category_list': categories,
            'products_recommended': products,
            'cart_obj': cart,
            'cart_items': cart_items,
            'login_form': login_form,
            'register_form': register_form,
            'cart': cart
                }

    return render(request, 'home_page.html', context)


# def about_page(request):
#     context =   {
#                     'title':'Acerca!',
#                     'content':'Acerca de nosotros',
#                 }
#     return render(request, 'home_page.html', context)

def contact_page(request):
    contact_form = ContactForm(request.POST or None)

    context =   {
                    'title': 'Contacto',
                    'content': 'Pagina de contacto',
                    'form': contact_form,
                }

    if contact_form.is_valid():
        # print(contact_form.cleaned_data)
        if request.is_ajax():
            return JsonResponse({"message": "Gracias por su tiempo!"})

    if contact_form.errors:
        # print(contact_form.cleaned_data)
        errors = contact_form.errors.as_json()
        if request.is_ajax():
            return HttpResponse(errors,status=400,content_type='application/json')

    return render(request,'contact/view.html',context)
