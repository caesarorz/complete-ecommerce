import random
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import Http404, HttpResponse
from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, get_object_or_404, redirect

from analytics.mixins import ObjectViewMixin
from carts.models import Cart, CartItem
from .models import Product, Variation#, ProductFile
from .forms import VariationInventoryFormSet
from .mixins import StaffRequiredMixin, LoginRequiredMixin


class ProductDetailViewAlter(DetailView):
    model = Product
    template_name = "products/product_detail_alt.html"

    def get_context_data(self, *args, **kwargs):
        print("ProductDetailViewAlter")
        context = super(ProductDetailViewAlter, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        instance = self.get_object()
        context['related'] = sorted(Product.objects.get_related(instance)[:6], key= lambda x: random.random())
        return context


class ProductListViewAlter(ListView):
    model = Product
    template_name = "products/product_list_alt.html"

    def get_context_data(self, *args, **kwargs):
        print("ProductListViewAlter")
        context = super(ProductListViewAlter, self).get_context_data(*args, **kwargs)
        cart_id = self.request.session.get("cart_id")
        print("cart_id",cart_id)
        return context




class VariationListView(StaffRequiredMixin, ListView):
    model = Variation

    template_name = "products/variation_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(VariationListView, self).get_context_data(*args, **kwargs)
        context["formset"] = VariationInventoryFormSet(queryset=self.get_queryset())
        return context

    def get_queryset(self, *args, **kwargs):
        product_pk = self.kwargs.get("pk")
        if product_pk:
            product = get_object_or_404(Product, pk=product_pk)
            queryset = Variation.objects.filter(product=product)
        return queryset

    def post(self, request, *args, **kwargs):
        formset = VariationInventoryFormSet(request.POST, request.FILES)
        pk = self.get_queryset()
        print(request.POST)
        if formset.is_valid():
            formset.save(commit=False)
            for form in formset:
                new_item = form.save(commit=False)
                if new_item.title:
                    product_pk = self.kwargs.get("pk")
                    product = get_object_or_404(Product, pk=product_pk)
                    new_item.product = product
                    new_item.save()

            messages.success(request, "Su inventario y precios ha sido salvado")
            return redirect("products:product_list")
        raise Http404


# class ProductFeaturedListView(ListView):
#     # queryset = Product.objects.all()
#     template_name = "products/list.html"
#
#     def get_queryset(self, *args, **kwargs):
#         request = self.request
#         return Product.objects.all().featured()
#
# class ProductFeaturedDetailView(ObjectViewMixin, DetailView):
#     queryset = Product.objects.all().featured()
#     template_name = "products/featured-detail.html"

    # def get_queryset(self,*args,**kwargs):
    #     request = self.request
    #     return Product.objects.featured()

class UserProductHistoryView(LoginRequiredMixin, ListView):
    template_name = "products/user-history.html"

    def get_context_data(self, *args, **kwargs):
        context = super(UserProductHistoryView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        # views = request.user.objectviewed_set.by_model(Product, model_queryset=False)  # all().filter(content_type__name='product')
        views = request.user.objectviewed_set.by_model(Variation) #all().filter(content_type='product')  # all().filter(content_type__name='product')
        print(views)
        viewed_ids = [x.object_id for x in views]
        # return Product.objects.filter(pk__in=viewed_ids)


class ProductListView(ListView):
    # queryset = Product.objects.all()
    # template_name = "products/list.html"
    template_name = "products/product_list_alt.html"

    def get_context_data(self, *args, **kwargs):
        print("ProductListView")
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all()

# def product_list_view(request):
#     queryset = Product.objects.all()
#     context = {
#         'object_list': queryset
#     }
#     return render(request, "products/list.html", context)


class ProductDetailSlugView(ObjectViewMixin, DetailView):
    queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        instance = self.get_object()
        context['related'] = Product.objects.get_related(instance)
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        # instance = get_object_or_404(Product, slug=slug, active=True) #Product.objects.get_by_id(pk)
        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404("Not found..")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("Ummmm")
        return instance



class ProductDetailView(ObjectViewMixin, DetailView):
    # queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        instance = Product.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Producto no existe")
        return instance
