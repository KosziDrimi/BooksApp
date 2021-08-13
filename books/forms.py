from django import forms
from .models import Book


def is_positive(num):
    return num != 0


def is_10_or_13(char):
    return len(char) == 10 or len(char) == 13


def is_digit(char):
    return char.isdigit()


def is_alpha_or_space(char):
    chars = [True for c in char if c.isalpha() or c.isspace()]
    return len(chars) == len(char)


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

    def clean_tytuł(self):
        data = self.cleaned_data.get('tytuł')

        if not is_alpha_or_space(data):
            raise forms.ValidationError('Tytuł musi składać się wyłącznie '
                                        'z liter oraz spacji.')

        return data

    def clean_autor(self):
        data = self.cleaned_data.get('autor')

        if not is_alpha_or_space(data):
            raise forms.ValidationError('Pole "autor" musi składać się '
                                        'wyłącznie z liter oraz spacji.')

        return data

    def clean_numer_isbn(self):
        data = self.cleaned_data.get('numer_isbn')

        if not is_10_or_13(data) or not is_digit(data):
            raise forms.ValidationError('Numer musi składać się z 10 lub 13 '
                                        'cyfr.')

        return data

    def clean_liczba_stron(self):
        data = self.cleaned_data.get('liczba_stron')

        if not is_positive(data):
            raise forms.ValidationError('Liczba stron musi być wartością '
                                        'dodatnią.')

        return data

    def clean_język_publikacji(self):
        data = self.cleaned_data.get('język_publikacji')

        if not is_alpha_or_space(data):
            raise forms.ValidationError('Pole "język" musi składać się '
                                        'wyłącznie z liter.')

        return data


class DateInput(forms.DateInput):
    input_type = 'date'


class FilterForm(forms.Form):
    tytuł = forms.CharField(required=False)
    autor = forms.CharField(required=False)
    język_publikacji = forms.CharField(required=False)
    data_początkowa = forms.DateField(widget=DateInput(), required=False)
    data_końcowa = forms.DateField(widget=DateInput(), required=False)


class APIForm(forms.Form):
    słowo_kluczowe = forms.CharField(max_length=50)
