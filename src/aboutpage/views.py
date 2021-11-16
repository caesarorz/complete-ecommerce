from django.shortcuts import render,redirect

from slideshow.models import Carousel, Slide

# Create your views here.

def about_page(request):

    about = Slide.objects.filter(carousel__title="Nosotros")
    context =   {
                    'about_slides': about,
                    'title':'Acerca!',
                    'content':'Acerca de nosotros',
                }

    return render(request, 'aboutpage/about.html', context)
