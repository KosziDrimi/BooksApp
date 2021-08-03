from django.db import models


class Book(models.Model):
    tytuł = models.CharField(max_length=50)
    autor = models.CharField(max_length=30)
    data_publikacji = models.DateField(help_text='yyyy-mm-dd')
    numer_isbn = models.CharField(max_length=20, verbose_name='Numer ISBN')
    liczba_stron = models.IntegerField(default=0)
    link_do_okładki = models.URLField()
    język_publikacji = models.CharField(max_length=20)

    def __str__(self):
        return self.tytuł
