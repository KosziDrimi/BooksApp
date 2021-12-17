from django_filters import FilterSet, DateFilter, CharFilter
from django import forms

from .models import Book


class DateInput(forms.DateInput):
    input_type = 'date'
    
    
class BookFilter(FilterSet):
    title = CharFilter(field_name='tytuł', lookup_expr='icontains', label='Tytuł')
    author = CharFilter(field_name='autor__nazwisko', lookup_expr='icontains', label='Autor')
    start_date = DateFilter(field_name='data_publikacji', lookup_expr='gte',
                            label='Data początkowa', widget=DateInput())
    end_date = DateFilter(field_name='data_publikacji', lookup_expr='lte',
                          label='Data końcowa', widget=DateInput())
    
    class Meta:
        model = Book
        fields = ['język_publikacji', 'numer_isbn']
