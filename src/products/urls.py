from django.conf.urls import url

from .views import (
                ProductListView,
                ProductDetailSlugView,
                # ProductDownloadView,
                VariationListView,
                # product_detail_view_alter,
                ProductDetailViewAlter,
                ProductListViewAlter,
                )

app_name = "products"

urlpatterns = [
    url(r'^alter/$', ProductListViewAlter.as_view(), name='product_list'),
    url(r'^(?P<slug>[\w-]+)/$', ProductDetailViewAlter.as_view(), name='product_detail'),
    url(r'^$', ProductListView.as_view(), name='list'),
    # url(r'^(?P<pk>\d+)', product_detail_view_alter, name='product_detail_function'),
    url(r'^(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/inventory/$', VariationListView.as_view(), name='inventory'),
    # url(r'^(?P<slug>[\w-]+)/(?P<pk>\d+)/$', ProductDownloadView.as_view(), name='download'),
]
