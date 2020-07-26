from flask import Flask, jsonify, request
from .models import setup_db, Book
from flask_cors import CORS


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    # CORS(app, resources={r'*/api/*':{origins: '*'}})

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PUT, PATCH, DELETE, OPTIONS')
        return response

    # To specify the number of books per shelf to display in each page
    books_per_shelf = 2

    def paginate_books(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * books_per_shelf
        end = start + books_per_shelf

        books = [book.format() for book in selection]
        current_books = books[start:end]

        return current_books

    @app.route('/books')
    def get_books():

        selection = Book.query.order_by(Book.id).all()
        current_books = paginate_books(request, selection)

        if len(current_books) == 0:
            return not_found(404)

        return jsonify({
            'success': True,
            'books': current_books,
            'total_books': len(Book.query.all())
        })

    @app.route('/books/<int:book_id>')
    def get_specific_book(book_id):

        book = Book.query.filter(Book.id == book_id).one_or_none()

        if book is None:
            return not_found(404)
            
        return jsonify({
            'success': True,
            'book': book.format()
        })

    @app.route('/books/<int:book_id>', methods=['PATCH'])
    def update_book(book_id):

        body = request.get_json()

        try:
            book = Book.query.filter(Book.id == book_id).one_or_none()

            if book is None:
                return not_found(404)

            if 'rating' in body:
                book.rating = int(body.get('rating'))

            if 'author' in body:
                book.author = body.get('author')

            if 'title' in body:
                book.title = body.get('title')

            book.update()

            return jsonify({
                'success': True,
                'id': book.id
            })

        except:
            bad_request(400)

    @app.route('/books/<int:book_id>', methods=['DELETE'])
    def delete_book(book_id):
        try:
            book = Book.query.filter(Book.id == book_id).one_or_none()

            if book is None:
                return not_found(404)

            book.delete()
            selection = Book.query.order_by(Book.id).all()
            current_books = paginate_books(request, selection)

            return jsonify({
                'success': True,
                'deleted': book_id,
                'books': current_books,
                'total_books': len(Book.query.all())
            })

        except:
            unprocessable(422)

    @app.route('/books', methods=['POST'])
    def create_book():

        body = request.get_json()

        new_author = body.get('author', None)
        new_title = body.get('title', None)
        new_rating = body.get('rating', None)
        search = body.get('search', None)

        try:
            if search:
                selection = Book.query.order_by(Book.id).filter(Book.title.ilike('%{}%'.format(search))).all()
                current_books = paginate_books(request, selection)

                if current_books == []:
                    current_books = 0

                return jsonify({
                    'success': True,
                    'books': current_books,
                    'total_books': len(selection)
                })

            else:
                book = Book(author=new_author, title=new_title, rating=int(new_rating))
                book.insert()

                selection = Book.query.order_by(Book.id).all()
                current_books = paginate_books(request, selection)

                return jsonify({
                    'success': True,
                    'created_book_id': book.id,
                    'books': current_books,
                    'total_books': len(Book.query.all())
                })

        except:
            unprocessable(422)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not Found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Entity"
        }), 422

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method Not Allowed"
        }), 405
    return app
