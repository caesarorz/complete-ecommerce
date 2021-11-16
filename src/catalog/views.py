from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, get_object_or_404, redirect

import random

from products.models import Product

from .models import Catalog, CatalogCategory


# class CategoryFeaturedListView(ListView):
#     def get_queryset(self, *args, **kwargs):
#         request = self.request
#         return CatalogCategory.objects.all().featured()
#
# class CategoryFeaturedDetailView(DetailView):
#     queryset = CatalogCategory.objects.all().featured()
    # template_title = "catalog/featured_category_detail.html"

    # def get_queryset(self, *args, **kwargs):
    #     request = self.request
    #     return CatalogCategory.objects.featured()



class CategoryListView(ListView):
    """
    List all categories in the main webpage
    """
    template_name = "catalog/category_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryListView, self).get_context_data(*args, **kwargs)
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return CatalogCategory.objects.all().active()


def category_list_view(request, pk=None, *args, **kwargs):
    queryset = CatalogCategory.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, "catalog/category_list.html", context)


# def get_products_category(self, *args, **kwargs):
#     pk = self.kwargs.get('pk')
#     instance = CatalogCategory.get_object(pk=pk)
#     products = Product.objects.filter(category__title=instance)
#     # instance = CatalogCategory.objects.get_by_id(pk)
#     print(products)
#     if products.count() <= 0:
#         raise Http404("No hay productos asignados")
#     return products


# class ProductDetailView(DetailView):
# 	model = Product
# 	#template_name = "product.html"
# 	#template_name = "<appname>/<modelname>_detail.html"
# 	def get_context_data(self, *args, **kwargs):
# 		context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
# 		instance = self.get_object()
# 		#order_by("-title")
# 		context["related"] = sorted(Product.objects.get_related(instance)[:6], key= lambda x: random.random())
# 		return context


class CategoryDetailSlugView(DetailView):
    queryset = CatalogCategory.objects.all()
    template_name = "catalog/category_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryDetailSlugView, self).get_context_data(*args, **kwargs)
        instance = self.get_object()
        products = Product.objects.filter(category__title=instance).active()
        # products = Product.objects.filter(category__title=instance)
        # cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['products'] = products
        return context

    def get_object(self, *args, **kwargs):
        # request = self.request
        slug = self.kwargs.get('slug')
        instance = get_object_or_404(CatalogCategory, slug=slug, active=True)
        # print(instance)
        if instance is None:
            raise Http404("Categoria no existe")
        return instance


class CategoryDetailView(DetailView):
    """
    List just the category selected with its products
    """
    template_name = "catalog/category_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(*args, **kwargs)
        # print(kwargs)
        instance = self.get_object()
        # order_by("-title")
        context["related"] = sorted(Product.objects.get_related(instance)[:6], key= lambda x: random.random())
        return context

    def get_object(self, *args, **kwargs):
        # request = self.request
        pk = self.kwargs.get('pk')
        instance = CatalogCategory.objects.get_by_id(pk)
        # print(instance)
        if instance is None:
            raise Http404("Categoria no existe")
        return instance


    #
    # def get_queryset(self, *args, **kwargs):
    #     request = self.request
    #     pk = self.kwargs.get('pk')
    #     return CatalogCategory.objects.filter(pk=pk)


def category_detail_view(request, pk=None, *args, **kwargs):
    # instance = CatalogCategory.objects.get(pk=pk, featured=True)
    # instance = get_object_or_404(CatalogCategory, pk=pk, featured=True)
    instance = CatalogCategory.objects.get_by_id(pk)
    if instance is None:
        raise Http404("Categoria no existe")

    products_list = Product.objects.filter(category__title=instance)

    print(products_list)

    context = {
        'object': instance,
        'products': products_list
    }
    return render(request, "catalog/category_detail.html", context)
