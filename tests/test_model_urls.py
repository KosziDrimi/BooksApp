from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve

from books.views import index, add, SearchResultView
from books.models import Book


class TestIndexURL(SimpleTestCase):

    def test_index_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_index_url_resolves(self):
        url = reverse('index')
        self.assertEqual(resolve(url).func, index)


class TestURLs(SimpleTestCase):

    def test_add_url_resolves(self):
        url = reverse('add')
        self.assertEqual(resolve(url).func, add)

    def test_show_url_resolves(self):
        url = reverse('show')
        self.assertEqual(resolve(url).func.__name__, SearchResultView.as_view().__name__)


class TestModel(TestCase):

    def test_model_str(self):
        book = Book.objects.create(tytuł='Test Title', autor='Test Author',
                                   data_publikacji='2010-01-01',
                                   numer_isbn='1234567890',
                                   link_do_okładki='https://www.google.com/',
                                   język_publikacji='pl')
        self.assertEqual(book.__str__(), 'Test Title')
        self.assertIsInstance(book, Book)
