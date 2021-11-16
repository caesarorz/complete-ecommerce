import random
import os
from django.db import models
from ecommerce.utils import unique_slug_generator, get_filename

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    new_filename = random.randint(1,3966666)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "slide/{new_filename}/{final_filename}".format(
                    new_filename=new_filename,
                    final_filename=final_filename
                    )


class Slide(models.Model):
        title                   = models.CharField(max_length=220, null=True, blank=True)
        message                 = models.TextField(null=True, blank=True)
        image                   = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
        active                  = models.BooleanField(default=True)
        timestamp               = models.DateTimeField(auto_now_add=True)
        bootstrap_class_active  = models.CharField(max_length=220, null=True, blank=True)

        def __str__(self):
            return self.title

        def get_id(self):
            id = self.id
            return id - 1

class Carousel(models.Model):
        carouselement           = models.ManyToManyField(Slide, verbose_name="Slideshow")
        title                   = models.CharField(max_length=220, null=True, blank=True)

        def __str__(self):
            return self.title
