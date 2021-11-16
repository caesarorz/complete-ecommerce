from django.conf.urls import url

from catalog.views import   (
                CategoryListView,
                CategoryDetailSlugView,
                            )

app_name = "categories"

urlpatterns = [
    url(r'^$', CategoryListView.as_view(), name='category_list'),
    url(r'^(?P<slug>[\w-]+)/$', CategoryDetailSlugView.as_view(), name='category_detail'),
    # url(r'^$', category_list_view),
    # url(r'^(?P<pk>\d+)/$', category_detail_view),
]
