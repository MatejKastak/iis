import django_filters

from .models import Borrowing
from .forms import BorrowingForm

class BorrowingAdminFilter(django_filters.FilterSet):

    class Meta:
        model = Borrowing
        fields = ['event', 'employee_borrowed', 'customer', 'costume', 'accessory']

class BorrowingUserFilter(django_filters.FilterSet):

    class Meta:
        model = Borrowing
        fields = ['event', 'costume', 'accessory']
