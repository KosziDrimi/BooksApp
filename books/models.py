from django.db import models


class Autor(models.Model):
    nazwisko = models.CharField(max_length=30, verbose_name='Autor')

    def __str__(self):
        return self.nazwisko


class Book(models.Model):
    tytuł = models.CharField(max_length=50)
    autor = models.ForeignKey(Autor, on_delete=models.DO_NOTHING)
    data_publikacji = models.DateField(help_text='yyyy-mm-dd')
    numer_isbn = models.CharField(max_length=20, verbose_name='Numer ISBN')
    liczba_stron = models.PositiveSmallIntegerField(default=0)
    link_do_okładki = models.URLField()
    język_publikacji = models.CharField(max_length=20)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.tytuł
