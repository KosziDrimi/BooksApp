from django.db import models


class Book(models.Model):
    tytuł = models.CharField(max_length=250)
    data_publikacji = models.DateField(help_text='yyyy-mm-dd')
    numer_isbn = models.CharField(max_length=50, verbose_name='Numer ISBN')
    liczba_stron = models.PositiveSmallIntegerField(default=0)
    link_do_okładki = models.URLField()
    język_publikacji = models.CharField(max_length=20)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.tytuł


class Autor(models.Model):
    nazwisko = models.CharField(max_length=250, verbose_name='Autor')
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.nazwisko
