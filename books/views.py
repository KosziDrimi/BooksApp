from django.shortcuts import render, redirect
from django.views.generic import ListView
from rest_framework import viewsets
from django_filters.views import FilterView
from django_filters.rest_framework import DjangoFilterBackend
import requests
from datetime import datetime


from .models import Book
from .forms import BookForm, APIForm
from .filters import BookFilter
from .serializers import BookSerializer
from myproject.settings import API_KEY


class BookList(ListView):
    model = Book
    paginate_by = 10


class SearchResultView(FilterView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'books/show.html'
    filterset_class = BookFilter
    paginate_by = 5

                        
class BookView(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('tytuł', 'autor', 'język_publikacji', 'data_publikacji')


def index(request):
    return render(request, 'books/index.html')


def add(request):
    if request.method == 'POST':
        form = BookForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('list')

    else:
        form = BookForm()

    context = {'form': form}
    return render(request, 'books/add_form.html', context)


def update(request, pk):
    book = Book.objects.get(id=pk)
    form = BookForm(instance=book)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)

        if form.is_valid():
            form.save()
            return redirect('list')

    context = {'form': form}
    return render(request, 'books/add_form.html', context)


def delete(request, pk):
    book = Book.objects.get(id=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('list')

    context = {'book': book}
    return render(request, 'books/delete.html', context)


def api_import(request):
    url = 'https://www.googleapis.com/books/v1/volumes?q={}&key={}'
    api_key = API_KEY

    if request.method == 'POST':
        form = APIForm(request.POST)

        if form.is_valid():
            query = form.cleaned_data['słowo_kluczowe']
            r = requests.get(url.format(query, api_key)).json()

            books = []
            data = r['items']
            for item in data:
                i = {}
                i['tytuł'] = item['volumeInfo']['title']
                i['język_publikacji'] = item['volumeInfo']['language']

                if 'authors' in item['volumeInfo']:
                    i['autor'] = item['volumeInfo']['authors'][0]
                else:
                    i['autor'] = 'brak danych'

                if 'pageCount' in item['volumeInfo']:
                    i['liczba_stron'] = item['volumeInfo']['pageCount']
                else:
                    i['liczba_stron'] = 0

                if 'industryIdentifiers' in item['volumeInfo']:
                    i['numer_isbn'] = (item['volumeInfo']
                                           ['industryIdentifiers'][0]
                                           ['identifier'])
                else:
                    i['numer_isbn'] = 'brak danych'

                if 'imageLinks' in item['volumeInfo']:
                    i['link_do_okładki'] = (item['volumeInfo']['imageLinks']
                                                ['thumbnail'])
                else:
                    i['link_do_okładki'] = 'brak danych'

                if 'publishedDate' in item['volumeInfo']:
                    i['data_publikacji'] = item['volumeInfo']['publishedDate']
                else:
                    continue

                if len(i['data_publikacji']) == 4:
                    i['data_publikacji'] = datetime.strptime(
                                        i['data_publikacji'], "%Y").date()
                elif len(i['data_publikacji']) == 7:
                    i['data_publikacji'] = datetime.strptime(
                                        i['data_publikacji'], "%Y-%m").date()
                else:
                    i['data_publikacji'] = i['data_publikacji']

                book = Book(tytuł=i['tytuł'], autor=i['autor'],
                            data_publikacji=i['data_publikacji'],
                            numer_isbn=i['numer_isbn'],
                            liczba_stron=i['liczba_stron'],
                            link_do_okładki=i['link_do_okładki'],
                            język_publikacji=i['język_publikacji'])

                book.save()
                books.append(book)

            context = {'books': books}
            return render(request, 'books/api_show.html', context)

    else:
        form = APIForm()

    context = {'form': form}
    return render(request, 'books/api_form.html', context)
