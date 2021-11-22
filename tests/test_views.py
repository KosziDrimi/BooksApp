from django.test import TestCase
from django.urls import reverse

from books.models import Book


class TestViews(TestCase):

    def test_add_view_GET(self):
        url = reverse('add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/add_form.html')

    def test_add_view_POST(self):
        url = reverse('add')
        data = {'tytuł': 'Test Title', 'autor': 'Test Author',
                'data_publikacji': '2010-01-01', 'numer_isbn': '1234567890',
                'liczba_stron': 111, 'język_publikacji': 'pl',
                'link_do_okładki': 'https://www.google.com/'}
        Book.objects.create(**data)
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Book.objects.first().tytuł, 'Test Title')
        self.assertEqual(Book.objects.first().numer_isbn, '1234567890')

    def test_show_view_GET(self):
        url = reverse('show')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/show.html')


    def test_delete_view_GET(self):
        Book.objects.create(tytuł='Test Title', autor='Test Author',
                            data_publikacji='2010-01-01',
                            numer_isbn='1234567890',
                            liczba_stron=111, język_publikacji='pl',
                            link_do_okładki='https://www.google.com/')
        url = reverse('delete', kwargs={'pk': 1})
        response = self.client.get(url, {'id': 1})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/delete.html')

    def test_delete_view_POST(self):
        Book.objects.create(tytuł='Test Title', autor='Test Author',
                            data_publikacji='2010-01-01',
                            numer_isbn='1234567890',
                            liczba_stron=111, język_publikacji='pl',
                            link_do_okładki='https://www.google.com/')
        url = reverse('delete', kwargs={'pk': 1})
        response = self.client.post(url, {'id': 1}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Book.objects.count(), 0)
        self.assertRedirects(response, '/book_list/', status_code=302,
                             target_status_code=200,
                             fetch_redirect_response=True)

    def test_update_view_GET(self):
        Book.objects.create(tytuł='Test Title', autor='Test Author',
                            data_publikacji='2010-01-01',
                            numer_isbn='1234567890',
                            liczba_stron=111, język_publikacji='pl',
                            link_do_okładki='https://www.google.com/')
        url = reverse('update', kwargs={'pk': 1})
        response = self.client.get(url, {'id': 1})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/add_form.html')

    def test_update_view_POST(self):
        Book.objects.create(tytuł='Test Title', autor='Test Author',
                            data_publikacji='2010-01-01',
                            numer_isbn='1234567890',
                            liczba_stron=111, język_publikacji='pl',
                            link_do_okładki='https://www.google.com/')
        url = reverse('update', kwargs={'pk': 1})
        data = {'id': 1, 'tytuł': 'Title', 'autor': 'Test Author',
                'data_publikacji': '2010-01-01', 'numer_isbn': '1234567890123',
                'liczba_stron': 111, 'język_publikacji': 'pl',
                'link_do_okładki': 'https://www.google.com/'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Book.objects.count(), 1)
        self.assertRedirects(response, '/book_list/', status_code=302,
                             target_status_code=200,
                             fetch_redirect_response=True)
        self.assertEqual(Book.objects.first().tytuł, 'Title')
        self.assertEqual(Book.objects.first().numer_isbn, '1234567890123')

    def test_api_import_view_GET(self):
        url = reverse('api_import')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/api_form.html')

    def test_api_import_view_POST(self):
        url = reverse('api_import')
        data = {'słowo_kluczowe': 'Title'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
