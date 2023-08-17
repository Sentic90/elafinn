from dashboard.models import Hotel, CATEGORY, PaymentMethod, PAYMENT_TYPE
from django import forms
import django_filters


class HotelSidebarFilter(django_filters.FilterSet):

    # distance = django_filters.NumberFilter(lookup_expr=)
    category = django_filters.ChoiceFilter(choices=CATEGORY, field_name='category')
    location__hrm__lte = django_filters.NumberFilter(field_name='location__hrm', lookup_expr='lte')
    location__hrm__gte = django_filters.NumberFilter(field_name='location__hrm', lookup_expr='gte')
    location__hrm__range = django_filters.NumberFilter(field_name='location__hrm', lookup_expr='range')
    payment_methods__type = django_filters.ChoiceFilter(choices=PAYMENT_TYPE, 
        field_name='payment_methods__type', widget=forms.widgets.Select(attrs={'class':'form-select'}))
    
    class Meta:
        model = Hotel
        fields = {
            'category':['exact'],
        }

'''
class ProductFilter(django_filters.FilterSet):

    class Meta:
        model = Product
        fields = {
            'name': ['exact'],
            'release_date': ['isnull'],
        }
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.BooleanField: {
                'filter_class': django_filters.BooleanFilter,
                'extra': lambda f: {
                    'widget': forms.CheckboxInput,
                },
            },
        }
'''