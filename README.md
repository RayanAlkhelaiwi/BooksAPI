# Books API
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This is a books API that provides basic information of registered books, including their titles, authors and ratings.

The backend code follows [PEP-8 style guidelines](https://www.python.org/dev/peps/pep-0008/).

### Getting Started
- Base URL: Currently this backend app can only be run locally. It's hosted by default at `127.0.0.1:5000` which is set as a proxy in the fronend configuration.

- Authentication: This version of the application does not require one, nor API keys.

From the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file.

To run the application, run the following commands inside the backend folder, but outside `flaskr` folder:

```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

**~~Frontend~~ [Not Applicable]**

Inside the fontend folder, run the following commands to start the client:

```
npm install // Only once to install dependencies
npm start
```

By default, the frontend will run on `localhost:3000`.

**Tests**

To run tests, go to the backend folder and run the following commands:

```
dropdb bookshelf_test
createdb bookshelf_test
psql bookshelf_test < books.psql
python test_book_api.py
```

Omit the `dropdb` command for the first time running the tests.

### Error Handling
Errors are returned as JSON obejcts in the following format:

```json
{
  "error": 404, 
  "message": "Not Found", 
  "success": false
}
```

The Error types the API returns when requests fail are:
| HTTP Status Code | Response |
| ----------- | ----------- |
| 400 | Bad Request |
| 404 | Not Found |
| 405 | Method Not Allowed |
| 422 | Unprocessable Entity |

### Endpoints
**GET /books**

Returns a list of books objects, success value and total number of books. Results are paginated in groups of 5. Include a query argument to choose page number (e.g. `?page=1`).

* Sample Request:

```
curl -X GET http://127.0.0.1:5000/books
```

* Sample Response:

```json
{
  "books": [
    {
      "author": "Leila Slimani", 
      "id": 1, 
      "rating": 2, 
      "title": "Lullaby"
    }, 
    {
      "author": "Amitava Kumar", 
      "id": 2, 
      "rating": 4, 
      "title": "Immigrant, Montana"
    }, 
    {
      "author": "Madeline Miller", 
      "id": 3, 
      "rating": 1, 
      "title": "CIRCE"
    }, 
    {
      "author": "Tara  Westover", 
      "id": 4, 
      "rating": 4, 
      "title": "Educated: A Memoir"
    }, 
    {
      "author": "Kristin Hannah", 
      "id": 5, 
      "rating": 4, 
      "title": "The Great Alone"
    }
  ], 
  "success": true, 
  "total_books": 25
}
```

**POST /books**

Creates a new book by submitting the information for a title, author and rating. It returns the ID of the newely created book in the DB, the submitted information, success value, number of total books.

* Sample Request:

```
curl -X POST -H "Content-Type: application/json" -d '{"author":"Mark Manson", "title":"The Subtle Art of Not Giving a F*ck", "rating":"9"}' http://127.0.0.1:5000/books
```

* Sample Response:

```json
{
  "books": {
    "author": "Mark Manson",
    "id": 26,
    "rating": 5,
    "title": "The Subtle Art of Not Giving a F*ck"
  },
  "created_book_id": 26,
  "success": true,
  "total_books": 26
}
```

**DELETE /books/{book_id}**

Deletes the book with the given ID. Returns the ID of the deleted books, success value, list of current books, and current number of total books.

* Sample Request:

```
curl -X DELETE http://127.0.0.1:5000/books/26
```

* Sample Response:

```json
{
  "books": [
    {
      "author": "Leila Slimani",
      "id": 1,
      "rating": 2,
      "title": "Lullaby"
    },
    {
      "author": "Amitava Kumar",
      "id": 2,
      "rating": 4,
      "title": "Immigrant, Montana"
    },
    {
      "author": "Madeline Miller",
      "id": 3,
      "rating": 1,
      "title": "CIRCE"
    },
    {
      "author": "Tara  Westover",
      "id": 4,
      "rating": 4,
      "title": "Educated: A Memoir"
    },
    {
      "author": "Kristin Hannah",
      "id": 6,
      "rating": 5,
      "title": "The Great Alone"
    }
  ],
  "deleted": 26,
  "success": true,
  "total_books": 25
}
```

**PATCH /books/{book_id}**

Updates the information of the book with the given ID. Returns success value and the ID of the updated book.

* Sample Request:

```
curl http://127.0.0.1:5000/books/4 -X PATCH -H "Content-Type: application/json" -d '{"author":"Tara  Westover", "title":"Educated: A Memoir", "rating":"4"}'
```

* Sample Response:

```json
{
  "id": 4,
  "success": true
}
```
