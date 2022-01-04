from django import forms
from .models import Autor, Book


def is_10_or_13(char):
    return len(char) == 10 or len(char) == 13


def is_alpha_space_or_dot(char):
    chars = [True for c in char if c.isalpha() or c.isspace() or c == '.' or c == '-']
    return len(chars) == len(char)


def is_not_digit(char):
    chars = [True for c in char if not c.isdigit()]
    return len(chars) == len(char)


class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = '__all__'

    def clean_nazwisko(self):
        data = self.cleaned_data.get('nazwisko')

        if not is_alpha_space_or_dot(data):
            raise forms.ValidationError('Pole "autor" musi składać się z liter oraz spacji plus '
                                        'ew kropki(ek) i/lub myślnika.')

        return data


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ['autor']

    def clean_tytuł(self):
        data = self.cleaned_data.get('tytuł')

        if not is_not_digit(data):
            raise forms.ValidationError('Tytuł nie może zawierać cyfr.')

        return data

    def clean_numer_isbn(self):
        data = self.cleaned_data.get('numer_isbn')

        if not is_10_or_13(data) or not data.isdigit():
            raise forms.ValidationError('Numer musi składać się z 10 lub 13 cyfr.')

        return data

    def clean_język_publikacji(self):
        data = self.cleaned_data.get('język_publikacji')

        if not data.isalpha():
            raise forms.ValidationError('Pole "język" musi składać się wyłącznie z liter.')

        return data


class APIForm(forms.Form):
    słowo_kluczowe = forms.CharField(max_length=250)
