import unittest, json, os
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from flaskr import setup_db, Book

class BookAPITestCase(unittest.TestCase):
    """ This class represents the Book API test cases """

    def setUp(self):
        """ Executed before each test.
        
        It defines the test variables, initializing the app,
        and setting up any other context that maybe needed (e.g. databases) """
        
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'books_db_test'
        self.database_path = 'postgres://{}/{}'.format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # Inserting a book
        self.new_book = {
            'author': 'Neil Gaiman',
            'title': 'Anansi Boys',
            'rating': 5
        }

        # Binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """ Executed after each test """
        
        pass

    def test_get_paginated_books(self):
        """ Test for getting successful paginated books """
        
        res = self.client().get('/books')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_books'])
        self.assertTrue(len(data['books']))

    def test_404_requesting_beyond_valid_pagination(self):
        """ Test for 404 requesting beyond valid pagination """
        
        res = self.client().get('/books?page=1000', json={'rating': 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    def test_get_specific_book(self):
        """ Test for getting specific book """

        res = self.client().get('/books/19')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_get_nonexistent_book(self):
        """ Test for 404 getting a nonexistent book """

        res = self.client().get('/books/300')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    def test_update_book(self):
        """ Test for updating a book """

        res = self.client().patch('/books/19', json=self.new_book)
        data = json.loads(res.data)
        book = Book.query.filter(Book.id == 19).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(book.format()['author'], 'Neil Gaiman')
        self.assertEqual(book.format()['title'], 'Anansi Boys')
        self.assertEqual(book.format()['rating'], 5)

    def test_400_update_book_bad_request(self):
        """ Test for 400 updating a book with no info passed (Bad Request) """

        res = self.client().patch(
            '/books/19', headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    def test_404_update_nonexistent_book(self):
        """ Test for 404 updating a nonexistent book """

        res = self.client().patch(
            '/books/300', json=self.new_book)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    def test_delete_book(self):
        """ Test for deleting a book """

        #! Increment book_id before execution
        book_id = 65

        res = self.client().delete('/books/' + str(book_id))
        data = json.loads(res.data)

        book = Book.query.filter(Book.id == book_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], book_id)
        self.assertTrue(data['books'])
        self.assertTrue(data['total_books'])
        self.assertEqual(book, None)

    def test_404_deleting_nonexistent_book(self):
        """ Test for 404 deleting a nonexistent book """

        res = self.client().delete('/books/300')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    def test_create_book(self):
        """ Test for creating a book """

        res = self.client().post(
            '/books', json=self.new_book)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created_book_id'])
        self.assertTrue(data['total_books'])

    def test_405_create_nonexistent_book(self):
        """ Test for 405 creating a nonexistent book """

        res = self.client().post(
            '/books/300', json=self.new_book)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method Not Allowed')

    def test_search_by_title_with_results(self):
        """ Test for searching a book by its title with results returned """

        res = self.client().post('/books', json={'search':'Anansi Boys'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['books'])
        self.assertTrue(data['total_books'] > 0)

    def test_search_by_title_no_results(self):
        """ Test for searching a book by its title that returns no results """

        res = self.client().post('/books', json={'search':'The Power of Habits'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['books'], 0)
        self.assertEqual(data['total_books'], 0)

    def test_404_search_nonexistent_title(self):
        """ Test for 404 search a nonexistent title """

        title = self.new_book['title']

        res = self.client().patch(
            '/books/search/titles', json=title)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

# To be able to execute the test case (i.e. 'python test_book_api.py')
if __name__ == '__main__':
    unittest.main()
