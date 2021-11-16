from django.conf.urls import url, include
from django.contrib import admin
from .views import (
            ProductListAPIView, 
            VariationListAPIView,
            VariationUpdateAPIView,
        )

app_name = "api"

urlpatterns = [
    url(r'^$', ProductListAPIView.as_view(), name='product-list'),
    url(r'^variations/$', VariationListAPIView.as_view(), name='variation-list'),
    url(r'^variations/(?P<pk>\d+)/$', VariationUpdateAPIView.as_view(), name='update'),
    ]

