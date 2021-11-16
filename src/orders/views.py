from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, JsonResponse, HttpResponse
from django.views.generic import ListView, View, DetailView
from django.shortcuts import render, get_object_or_404
from django.core.mail import EmailMessage

from billing.models import BillingProfile
from .models import Order, ProductPurchase
from ecommerce.utils import render_to_pdf
from carts.models import Cart, CartItem

from django.template.loader import get_template


class GenerateOrderPDF(DetailView):
    def get(self, request, *args, **kwargs):
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        user = billing_profile
        order_id = request.GET.get('order_id')
        if order_id:
            # order_obj = Order.objects.get_by_id(id=order_id)
            qs = Order.objects.all().filter(order_id=order_id, active=True)
            if qs.count() == 1:
                order_id = qs.first()
        items = ''

        for product in order_id.cart.cartitem_set.all():
            items += '{0:<20}  {1:>20}  {2:>20}\n'.format(
                            str(product),
                            str(product.quantity),
                            str(product.line_item_total))

        template = get_template("orders/order_detail_pdf.html")
        context = {
            'object': order_id,
            'name': user,
            'shipping_address': order_id.shipping_address.get_address(),
            'payment_method': order_id.payment_method,
            'items': items,
            # 'tax': order_id.
            'total': order_id.total,
        }
        html = template.render(context)
        pdf = render_to_pdf("orders/order_detail_pdf.html", context)
        if pdf:
            return HttpResponse(pdf, content_type='application/pdf')
        return HttpResponse("Not found")


class OrderListView(LoginRequiredMixin, ListView):

    def get_queryset(self):
        return Order.objects.by_request(self.request).not_created()


class OrderDetailView(LoginRequiredMixin, DetailView):

    def get_object(self):
        #return Order.objects.get(id=self.kwargs.get('id'))
        #return Order.objects.get(slug=self.kwargs.get('slug'))
        qs = Order.objects.by_request(
                    self.request
                ).filter(
                    order_id = self.kwargs.get('order_id')
                )
        if qs.count() == 1:
            return qs.first()
        raise Http404

# class LibraryView(LoginRequiredMixin, ListView):
#     template_name = 'orders/library.html'
#     def get_queryset(self):
#         return ProductPurchase.objects.products_by_request(self.request)  #by_request(self.request).digital()

class VerifyOwnership(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            data = request.GET
            product_id = request.GET.get('product_id', None)
            if product_id is not None:
                product_id = int(product_id)
                ownership_ids = ProductPurchase.objects.products_by_id(request)  #by_request(self.request).digital()
                if product_id in ownership_ids:
                    return JsonResponse({'owner': True})
            return JsonResponse({'owner': False})
        raise Http404
