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
    return "about/{new_filename}/{final_filename}".format(
                    new_filename=new_filename,
                    final_filename=final_filename
                    )


# class JumbotronQuerySet(models.query.QuerySet):
#     def active(self):
#         return self.filter(active=True)
#
# class JumbotronManager(models.Manager):
#     def get_queryset(self):
#         return JumbotronQuerySet(self.model, using=self._db)
#
#     def all(self):
#         return self.get_queryset().active()

# class Jumbotron(models.Model):
#     header_one            = models.CharField(max_length=220, default="Hello World")
#     paragraph             = models.TextField(blank=True, null=True)
#     image                 = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
#     active                = models.BooleanField(default=True)
#     timestamp             = models.DateTimeField(auto_now_add=True)
#     # title_btn           = models.CharField(max_length=50, default='Join')
#     # title_btn_url       = models.CharField(max_length=50, blank=True, null=True)
#     # content             = models.TextField(blank=True, null=True)
#     # show_nav            = models.BooleanField(default=True, help_text='Show Navigation Bar?')
#
#     def __str__(self):
#         return self.header_one
#
#     def get_id(self):
#         header_one = self.header_one.lower().replace(" ", "-")
#         return header_one
#
#     objects = JumbotronManager()


class About(models.Model):
    header_one            = models.CharField(max_length=220, default="Hello World")
    paragraph             = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.header_one
