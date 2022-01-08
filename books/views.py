from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.forms import modelformset_factory
from rest_framework import viewsets
from django_filters.views import FilterView
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
import requests
from datetime import datetime

from .models import Autor, Book
from .forms import AutorForm, BookForm, APIForm
from .filters import BookFilter
from .serializers import AutorSerializer, BookSerializer
from myproject.settings import API_KEY


class BookList(ListView):
    model = Book
    context_object_name = 'book_list'
    ordering = ['-id']
    paginate_by = 10


class BookFilterView(FilterView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'books/book_filter.html'
    ordering = ['-id']
    filterset_class = BookFilter
    paginate_by = 6


class AutorView(viewsets.ModelViewSet):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer


class BookView(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('tytuł', 'autor', 'język_publikacji', 'data_publikacji')


def index(request):
    return render(request, 'books/index.html')


def add(request):
    AutorFormSet = modelformset_factory(Autor, form=AutorForm, extra=1, min_num=1, validate_min=True)

    if request.method == 'POST':
        book_form = BookForm(request.POST)
        autor_formset = AutorFormSet(request.POST)

        if autor_formset.is_valid() and book_form.is_valid():

            data = book_form.cleaned_data
            try:
                book = Book.objects.filter(numer_isbn=data['numer_isbn']).get()
                messages.warning(request, 'Pozycja o tym numerze ISBN już widnieje w bazie.')
            except ObjectDoesNotExist:
                book = Book(**data)
                book.save()
                messages.warning(request, 'Pozycja dodana do bazy.')

            for form in autor_formset.cleaned_data:
                if len(form) > 0:
                    name = form['nazwisko']

                    try:
                        autor = Autor.objects.filter(nazwisko__iexact=name).get()
                    except ObjectDoesNotExist:
                        autor = Autor(nazwisko=name)
                        autor.save()
                    finally:
                        autor.books.add(book)

            return redirect('list')

    else:
        autor_formset = AutorFormSet(queryset=Autor.objects.none())
        book_form = BookForm()

    context = {'autor_form': autor_formset, 'book_form': book_form}
    return render(request, 'books/add_form.html', context)


def update(request, pk):
    book = Book.objects.get(id=pk)
    AutorFormSet = modelformset_factory(Autor, form=AutorForm, extra=1, min_num=1, validate_min=True)
    authors = Autor.objects.filter(books__id=pk)
    autor_formset = AutorFormSet(queryset=authors)
    form = BookForm(instance=book)

    if request.method == 'POST':
        autor_formset = AutorFormSet(request.POST, queryset=Autor.objects.filter(books__id=pk))
        form = BookForm(request.POST, instance=book)

        if form.is_valid() and autor_formset.is_valid():
            form.save()

            for author in authors:
                book.autor_set.remove(author)

            for form in autor_formset.cleaned_data:
                if len(form) > 0:
                    name = form['nazwisko']

                    try:
                        autor = Autor.objects.filter(nazwisko__iexact=name).get()
                    except ObjectDoesNotExist:
                        autor = Autor(nazwisko=name)
                        autor.save()
                    finally:
                        autor.books.add(book)

            messages.warning(request, 'Pozycja zaktualizowana.')
            return redirect('list')

    context = {'book_form': form, 'autor_form': autor_formset}
    return render(request, 'books/add_form.html', context)


def delete(request, pk):
    book = Book.objects.get(id=pk)
    book.delete()
    return redirect('list')


def api_import(request):
    url = 'https://www.googleapis.com/books/v1/volumes?startIndex=0&maxResults=20&q={}&key={}'
    api_key = API_KEY

    if request.method == 'POST':
        form = APIForm(request.POST)

        if form.is_valid():
            query = form.cleaned_data['słowo_kluczowe']
            r = requests.get(url.format(query, api_key)).json()

            books = []
            data = r['items']

            for item in data:
                tytuł = item['volumeInfo']['title']
                język_publikacji = item['volumeInfo']['language']
                autor = (item['volumeInfo']['authors'][0] if 'authors' in item['volumeInfo'] else 'brak danych')
                liczba_stron = (item['volumeInfo']['pageCount'] if 'pageCount' in item['volumeInfo'] else 0)
                numer_isbn = (item['volumeInfo']['industryIdentifiers'][0]['identifier'] if 'industryIdentifiers'
                                in item['volumeInfo'] else 'brak danych')
                link_do_okładki = (item['volumeInfo']['imageLinks']['thumbnail'] if 'imageLinks' in item['volumeInfo']
                                    else 'brak danych')

                if 'publishedDate' in item['volumeInfo']:
                    data_publikacji = item['volumeInfo']['publishedDate']
                else:
                    continue

                if len(data_publikacji) == 4:
                    try:
                        data_publikacji = datetime.strptime(data_publikacji, "%Y").date()
                    except ValueError:
                        continue
                elif len(data_publikacji) == 7:
                    data_publikacji = datetime.strptime(data_publikacji, "%Y-%m").date()

                try:
                    Autor.objects.filter(nazwisko__iexact=autor).get()
                except ObjectDoesNotExist:
                    author = Autor(nazwisko=autor)
                    author.save()

                try:
                    Book.objects.filter(numer_isbn=numer_isbn).get()
                except ObjectDoesNotExist:
                    book = Book(tytuł=tytuł,
                                autor=Autor.objects.filter(nazwisko__iexact=autor).get(),
                                data_publikacji=data_publikacji,
                                numer_isbn=numer_isbn,
                                liczba_stron=liczba_stron,
                                link_do_okładki=link_do_okładki,
                                język_publikacji=język_publikacji)
                    book.save()
                    books.append(book)

            context = {'book_list': books}
            return render(request, 'books/api_show.html', context)

    else:
        form = APIForm()

    context = {'form': form}
    return render(request, 'books/api_form.html', context)
