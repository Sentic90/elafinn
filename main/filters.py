from dashboard.models import Hotel, CATEGORY, PaymentMethod, PAYMENT_TYPE
from django import forms
import django_filters


DISTANCE_FILTER = {
        'less_than_1km':(0, 1),
        'between_5_10km': (5,10),
        'greater_than_10km': (10, 10000)
    }
class SidebarFilterForm(forms.Form):

    DISTANCE = [
        ((0,1), 'أقل من كيلو'),
        ((5,10), 'من 5 إلى 10 كيلو'),
        ((10,100000), '10 كيلو فأكثر'),
    ]

    CATEGORY_CHOICES = [
            ('0', '0 stars'),
            ('1', '1 star'),
            ('2', '2 stars'),
            ('3', '3 stars'),
            ('4', '4 stars'),
            ('5', '5 stars'),
        ]

    payment_method = forms.ChoiceField(choices=PAYMENT_TYPE)
    distance = forms.ChoiceField(choices=DISTANCE)
    category = forms.MultipleChoiceField(choices=CATEGORY_CHOICES, required=False, widget=forms.widgets.CheckboxSelectMultiple(
        attrs={
            'class': 'form-check-input'
        }))


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