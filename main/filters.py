from dashboard.models import Hotel, CATEGORY
import django_filters


class HotelSidebarFilter(django_filters.FilterSet):
    # distance = django_filters.NumberFilter(lookup_expr=)
    category = django_filters.ChoiceFilter(choices=CATEGORY, field_name='category')
    location__hrm__lte = django_filters.NumberFilter(field_name='location__hrm', lookup_expr='lte')
    location__hrm__gte = django_filters.NumberFilter(field_name='location__hrm', lookup_expr='gte')
    location__hrm_range = django_filters.NumericRangeFilter(field_name='location__hrm')
    class Meta:
        model = Hotel
        fields = {
            'category':['exact'],
        }
