from django_filters.rest_framework import FilterSet
from main.models import Product, Order
import django_filters


class ProductFilter(FilterSet):   # фильтрация продуктов по цене, по размеру,название

    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    size = django_filters.NumberFilter(field_name='size', lookup_expr='gte')
    price_from = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_to = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ('category', 'title', 'size', 'price_from', 'price_to')


class OrderFilter(FilterSet):

    """Фильтрация по сумме (от и до), по названию товару, по статусам, по дате"""
    total_sum_from = django_filters.NumberFilter(field_name='total_sum', lookup_expr='gte')
    total_sum_to = django_filters.NumberFilter(field_name='total_sum', lookup_expr='lte')
    created_at = django_filters.DateTimeFromToRangeFilter(field_name='created_at')
    product = django_filters.CharFilter(field_name='products__product__title', lookup_expr='icontains')

    class Meta:
        model = Order
        fields = ('total_sum_from', 'total_sum_to', 'created_at', 'product')