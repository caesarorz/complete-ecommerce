from rest_framework import serializers

from django.db.models import Q

from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin

from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)

from rest_framework.generics import (
                    RetrieveUpdateAPIView,
                    CreateAPIView,  # see comment at views
                    ListAPIView, 
                    RetrieveAPIView,
                    DestroyAPIView,
                    UpdateAPIView
                )

from .serializers import (
    ProductSerializer, 
    ProductListSerializer,
    VariationListSerializer,
    VariationCreateUpdateSerializer,
    )

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly
) 
from products.models import Product, Variation


class ProductListAPIView(ListAPIView):
    # queryset = Post.objects.all()
    serializer_class = ProductListSerializer
    # filter_backends = [SearchFilter, OrderingFilter]
    # search_fields = ['title', 'content', 'user__first_name']
    # pagination_class = PostPageNumberPagination
    # permission_classes = [AllowAny]

    def get_queryset(self, *args, **kwargs):
        # queryset_list = super(PostListAPIView, self).get_query_set(*args, **kwargs)
        queryset_list = Product.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query)
                # Q(content__icontains=query) |
                # Q(user__first_name__icontains=query) |
                # Q(user__last_name__icontains=query) 
            ).distinct()
        return queryset_list


class VariationListAPIView(ListAPIView):
    queryset = Variation.objects.all()
    serializer_class = VariationListSerializer


class VariationUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Variation.objects.all()
    serializer_class = VariationCreateUpdateSerializer 
    # permission_classes = [IsOwnerOrReadOnly]
    lookup_field = 'pk'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)