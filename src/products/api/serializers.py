
from rest_framework.serializers import (
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
) 

from products.models import Product, Variation

class ProductSerializer(ModelSerializer):
    url = SerializerMethodField(read_only=True)
    class Meta:
        model = Product
        fields = [
            'url',
            'pk',
            'category',
            'title',
            'slug',
            'description',
            'featured',
        ]
        read_only_field = ['id', 'user', 'pk']

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)

class ProductListSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = [
            # 'url',
            # 'id',
            'title',
            'slug',
            'description',
        ]
    
class VariationListSerializer(ModelSerializer):
    class Meta:
        model = Variation
        fields = [
            'pk',
            'product',
            'title',
            'inventory',
            'presentation',
        ]

class VariationCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Variation
        fields = [
            'pk',
            'product',
            'title',
            'inventory',
            'presentation',
        ]
        read_only_field = ['pk', 'product']