import django_filters
from dashboard.models import ContactUsNotificationFile
from django.db.models import Q


class ContactUsNotificationFileFilter(django_filters.FilterSet):
    contact_us_target = django_filters.CharFilter(field_name='contact_us_target', lookup_expr='iexact')
    contact_us_from_user = django_filters.CharFilter(field_name='contact_us_from_user',lookup_expr='iexact')

    class Meta:
        model = ContactUsNotificationFile
        fields = ('contact_us_target', 'contact_us_from_user')
