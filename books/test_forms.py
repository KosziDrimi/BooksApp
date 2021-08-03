from django.test import TestCase

from .models import Book
from .forms import BookForm


class TestBookForm(TestCase):

    def test_valid_book_form(self):
        book = Book.objects.create(tytuł='Test Title', autor='Test Author',
                                   data_publikacji='2010-01-01',
                                   numer_isbn='1234567890',
                                   liczba_stron=111, język_publikacji='pl',
                                   link_do_okładki='https://www.google.com/')

        data = {'tytuł': book.tytuł, 'autor': book.autor,
                'data_publikacji': book.data_publikacji,
                'numer_isbn': book.numer_isbn,
                'liczba_stron': book.liczba_stron,
                'link_do_okładki': book.link_do_okładki,
                'język_publikacji': book.język_publikacji}

        form = BookForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_book_form_title(self):
        book = Book.objects.create(tytuł='111Test#@Title963{}',
                                   autor='Test Author',
                                   data_publikacji='2010-01-01',
                                   numer_isbn='1234567890',
                                   liczba_stron=111, język_publikacji='pl',
                                   link_do_okładki='https://www.google.com/')

        data = {'tytuł': book.tytuł, 'autor': book.autor,
                'data_publikacji': book.data_publikacji,
                'numer_isbn': book.numer_isbn,
                'liczba_stron': book.liczba_stron,
                'link_do_okładki': book.link_do_okładki,
                'język_publikacji': book.język_publikacji}

        form = BookForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['tytuł'],
                                    ['Tytuł musi składać się wyłącznie z '
                                     'liter oraz spacji.'])

    def test_invalid_book_form_author(self):
        book = Book.objects.create(tytuł='Test Title', autor='1g4h6j3k8a',
                                   data_publikacji='2010-01-01',
                                   numer_isbn='1234567890',
                                   liczba_stron=111, język_publikacji='pl',
                                   link_do_okładki='https://www.google.com/')

        data = {'tytuł': book.tytuł, 'autor': book.autor,
                'data_publikacji': book.data_publikacji,
                'numer_isbn': book.numer_isbn,
                'liczba_stron': book.liczba_stron,
                'link_do_okładki': book.link_do_okładki,
                'język_publikacji': book.język_publikacji}

        form = BookForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['autor'],
                                    ['Pole "autor" musi składać się wyłącznie '
                                     'z liter oraz spacji.'])

    def test_invalid_book_form_isbn_lenght(self):
        book = Book.objects.create(tytuł='Test Title', autor='Test Author',
                                   data_publikacji='2010-01-01',
                                   numer_isbn='1234567',
                                   liczba_stron=111, język_publikacji='pl',
                                   link_do_okładki='https://www.google.com/')

        data = {'tytuł': book.tytuł, 'autor': book.autor,
                'data_publikacji': book.data_publikacji,
                'numer_isbn': book.numer_isbn,
                'liczba_stron': book.liczba_stron,
                'link_do_okładki': book.link_do_okładki,
                'język_publikacji': book.język_publikacji}

        form = BookForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['numer_isbn'],
                                    ['Numer musi składać się z 10 lub 13 '
                                     'cyfr.'])

    def test_invalid_book_form_isbn_digits(self):
        book = Book.objects.create(tytuł='Test Title', autor='Test Author',
                                   data_publikacji='2010-01-01',
                                   numer_isbn='orgbcted01',
                                   liczba_stron=111, język_publikacji='pl',
                                   link_do_okładki='https://www.google.com/')

        data = {'tytuł': book.tytuł, 'autor': book.autor,
                'data_publikacji': book.data_publikacji,
                'numer_isbn': book.numer_isbn,
                'liczba_stron': book.liczba_stron,
                'link_do_okładki': book.link_do_okładki,
                'język_publikacji': book.język_publikacji}

        form = BookForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['numer_isbn'],
                                    ['Numer musi składać się z 10 lub 13 '
                                     'cyfr.'])

    def test_invalid_book_form_negative_pages(self):
        book = Book.objects.create(tytuł='Test Title', autor='Test Author',
                                   data_publikacji='2010-01-01',
                                   numer_isbn='1234567890',
                                   liczba_stron=-111, język_publikacji='pl',
                                   link_do_okładki='https://www.google.com/')

        data = {'tytuł': book.tytuł, 'autor': book.autor,
                'data_publikacji': book.data_publikacji,
                'numer_isbn': book.numer_isbn,
                'liczba_stron': book.liczba_stron,
                'link_do_okładki': book.link_do_okładki,
                'język_publikacji': book.język_publikacji}

        form = BookForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['liczba_stron'],
                                    ['Liczba stron musi być wartością '
                                     'dodatnią.'])

    def test_invalid_book_form_language(self):
        book = Book.objects.create(tytuł='Test Title', autor='Test Author',
                                   data_publikacji='2010-01-01',
                                   numer_isbn='1234567890',
                                   liczba_stron=111, język_publikacji='pl456',
                                   link_do_okładki='https://www.google.com/')

        data = {'tytuł': book.tytuł, 'autor': book.autor,
                'data_publikacji': book.data_publikacji,
                'numer_isbn': book.numer_isbn,
                'liczba_stron': book.liczba_stron,
                'link_do_okładki': book.link_do_okładki,
                'język_publikacji': book.język_publikacji}

        form = BookForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['język_publikacji'],
                                    ['Pole "język" musi składać się wyłącznie '
                                     'z liter.'])
