import django_filters
from app01.models import Owner

class OwnerFilter(django_filters.rest_framework.FilterSet):
    name = django_filters.CharFilter(name="name", lookup_expr="icontains")
    phone = django_filters.CharFilter(name="name", lookup_expr="icontains")
    address = django_filters.CharFilter(name="address", lookup_expr="icontains")

    class Meta:
        model = Owner
        fields = ['name', 'phone', 'address']
