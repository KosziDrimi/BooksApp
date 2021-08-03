# BooksApp

Application to store books with the following details:
- title,
- author,
- date of the publication,
- ISBN number,
- number of pages,
- link to the cover,
- language of the publication.

It offers the possibility to (from the index view):
- manually add new titles,
- search for books (using title, author, language and/or period of publication filters),
- see the whole list of added books (in the table),
- import books from Google Books API.

And from the book_list view:
- update entries,
- delete entries. 

The api view connects to Django Rest Framework and allows:
- checking the whole list of books,
- adding, updating and deleting entries,
- filtering entries using query strings.

In order to see this project you should:
- install all required dependencies (`pip install -r requirements.txt`),
- run `python manage.py runserver` on your command line,
- and open the browser at local host specified. 

The application is also deployed to Heroku: https://koszidrimi-booksapp.herokuapp.com/.

Technologies: Python 3.8.3, Django 3.2.6, HTML5, Bootstrap 5.0.