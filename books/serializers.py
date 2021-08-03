from rest_framework import serializers

from .models import Book


class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'url', 'tytuł', 'autor', 'data_publikacji',
                  'numer_isbn', 'liczba_stron', 'link_do_okładki',
                  'język_publikacji')
