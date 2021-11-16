from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView, RedirectView

from accounts.views import LoginView, RegisterView, GuestRegisterView
from addresses.views import checkout_address_create_view, checkout_address_reuse_view
from billing.views import payment_method_view, payment_method_createview
from carts.views import (
            cart_detail_api_view,
            CartView, ItemCountView,
            CheckoutView,
            choose_payment_method,
            payment_cash,
            CartItemsList,
            create_payment_method
            )
from marketing.views import MarketingPreferenceUpdateView, MailchimpWebhookView
from orders.views import GenerateOrderPDF #LibraryView for future services (digital products)
from analytics.views import SalesView, SalesAjaxView
from contact.views import contact_page
from contact.api.views import ContactCreateAPIView
from aboutpage.views import about_page
from .views import home_page
# from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    url(r'i18n/', include('django.conf.urls.i18n')),
    url(r'^admin/', admin.site.urls),
    url(r'^$', home_page, name='home'),
    url(r'^about/$', about_page, name='about'),
    url(r'^accounts/$', RedirectView.as_view(url='/account')),
    url(r'^account/', include("accounts.urls", namespace='account')),
    url(r'^accounts/', include("accounts.passwords.urls")),
    url(r'^analytics/sales/$', SalesView.as_view(), name='/sales-analytics'),
    url(r'^analytics/sales/data/$', SalesAjaxView.as_view(), name='/sales-analytics-data'),
    url(r'^api/contact/$', ContactCreateAPIView.as_view(), name='contact-api'),
    url(r'^contact/$', contact_page, name='contact'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^checkout/address/create/$', checkout_address_create_view, name='checkout_address_create'),
    url(r'^checkout/address/reuse/$', checkout_address_reuse_view, name='checkout_address_reuse'),
    url(r'^checkout/payment/select/$', choose_payment_method, name='choose_payment_method'),
    url(r'^checkout/payment/create/$', create_payment_method, name='create_payment_method'),
    url(r'^checkout/payment/cash/$', payment_cash, name='payment_cash'),
    # url(r'^register/guest/$', GuestRegisterView.as_view(), name='guest_register'),
    url(r'^register/guest/$', GuestRegisterView.as_view(), name='guest_register'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    # url(r'^api/cart/$', cart_detail_api_view, name='api-cart'),
    url(r'^cart/', include(("carts.urls"), namespace='cart')),
    url(r'^cart-cbv/$', CartView.as_view(), name='cart-cbv'),  # cart class, experimental
    url(r'^cart-cbv/count/$', ItemCountView.as_view(), name='item_count'),  # cart class, experimental
    url(r'^cart-cbv/list/$', CartItemsList.as_view(), name='items_list'),  # cart class, experimental
    url(r'^checkout/$', CheckoutView.as_view(), name='checkout'),  # cart class, experimental
    url(r'^billing/payment-method/$', payment_method_view, name='billing-payment-method'),
    url(r'^billing/payment-method/create/$', payment_method_createview, name='billing-payment-method-endpoint'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    # url(r'^library/$', LibraryView.as_view(), name='library'), for future services (digital products)
    url(r'^orders/', include("orders.urls", namespace='orders')),
    url(r'^api/products/', include('products.api.urls', namespace='api-products')),
    url(r'^products/', include("products.urls", namespace='products')),
    url(r'^categories/', include("catalog.urls", namespace='categories')),
    url(r'^search/', include("search.urls", namespace='search')),
    # url(r'^settings/$', RedirectView.as_view(url='/account')),
    url(r'^settings/email/$', MarketingPreferenceUpdateView.as_view(), name='marketing-pref'),
    url(r'^webhooks/mailchimp/$', MailchimpWebhookView.as_view(), name='webhooks-mailchimp'),
    # prefix_default_language=False,
]

# urlpatterns += i18n_patterns (
#     url(r'^$', home_page, name='home'),
#     url(r'^about/$', about_page, name='about'),
#     url(r'^accounts/$', RedirectView.as_view(url='/account')),
#     url(r'^account/', include("accounts.urls", namespace='account')),
#     url(r'^accounts/', include("accounts.passwords.urls")),
#     url(r'^analytics/sales/$', SalesView.as_view(), name='/sales-analytics'),
#     url(r'^analytics/sales/data/$', SalesAjaxView.as_view(), name='/sales-analytics-data'),
#     url(r'^api/contact/$', ContactCreateAPIView.as_view(), name='contact-api'),
#     url(r'^contact/$', contact_page, name='contact'),
#     url(r'^login/$', LoginView.as_view(), name='login'),
#     url(r'^checkout/address/create/$', checkout_address_create_view, name='checkout_address_create'),
#     url(r'^checkout/address/reuse/$', checkout_address_reuse_view, name='checkout_address_reuse'),
#     url(r'^checkout/payment/select/$', choose_payment_method, name='choose_payment_method'),
#     url(r'^checkout/payment/create/$', create_payment_method, name='create_payment_method'),
#     url(r'^checkout/payment/cash/$', payment_cash, name='payment_cash'),
#     # url(r'^register/guest/$', GuestRegisterView.as_view(), name='guest_register'),
#     url(r'^register/guest/$', GuestRegisterView.as_view(), name='guest_register'),
#     url(r'^logout/$', LogoutView.as_view(), name='logout'),
#     # url(r'^api/cart/$', cart_detail_api_view, name='api-cart'),
#     url(r'^cart/', include("carts.urls", namespace='cart')),
#     url(r'^cart-cbv/$', CartView.as_view(), name='cart-cbv'),  # cart class, experimental
#     url(r'^cart-cbv/count/$', ItemCountView.as_view(), name='item_count'),  # cart class, experimental
#     url(r'^cart-cbv/list/$', CartItemsList.as_view(), name='items_list'),  # cart class, experimental
#     url(r'^checkout/$', CheckoutView.as_view(), name='checkout'),  # cart class, experimental
#     url(r'^billing/payment-method/$', payment_method_view, name='billing-payment-method'),
#     url(r'^billing/payment-method/create/$', payment_method_createview, name='billing-payment-method-endpoint'),
#     url(r'^register/$', RegisterView.as_view(), name='register'),
#     # url(r'^library/$', LibraryView.as_view(), name='library'), for future services (digital products)
#     url(r'^orders/', include("orders.urls", namespace='orders')),
#     url(r'^products/', include("products.urls", namespace='products')),
#     url(r'^categories/', include("catalog.urls", namespace='categories')),
#     url(r'^search/', include("search.urls", namespace='search')),
#     # url(r'^settings/$', RedirectView.as_view(url='/account')),
#     url(r'^settings/email/$', MarketingPreferenceUpdateView.as_view(), name='marketing-pref'),
#     url(r'^webhooks/mailchimp/$', MailchimpWebhookView.as_view(), name='webhooks-mailchimp'),
#     prefix_default_language=False,
# )

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
