from django_filters.rest_framework import FilterSet
from main.models import Product
import django_filters


class ProductFilter(FilterSet):   # фильтрация продуктов по цене, по размеру,название

    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    size = django_filters.NumberFilter(field_name='size', lookup_expr='gte')
    price_from = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_to = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ('category', 'title', 'size', 'price_from', 'price_to')

