from flask_app.config.mysqlconnection import connectToMySQL


from flask_app.models import author



class Book:

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.pages = data['pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.authors = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM books;"
        results = connectToMySQL('books').query_db(query)
        books = []
        for book in results:
            books.append( cls(book) )
        return books

    @classmethod
    def save( cls , data ):
        query = "INSERT INTO books ( title, pages, created_at , updated_at ) VALUES (%(title)s, %(pages)s, NOW(),NOW() );"
        return connectToMySQL('books').query_db( query, data )


    @classmethod
    def get_books_author( cls , data ):
        query = "SELECT * FROM books LEFT JOIN favorites ON favorites.book_id = books.id LEFT JOIN authors ON favorites.author_id = authors.id WHERE books.id = %(id)s;"
        results = connectToMySQL('books').query_db( query , data ) 
        book = cls( results[0] )
        for row in results:
            author_data = {
                "id" : row["authors.id"],
                "name" : row["name"],
                "created_at" : row["authors.created_at"],
                "updated_at" : row["authors.updated_at"]
            }
            book.authors.append( author.Author( author_data ) )
        return book

    @classmethod
    def addfavoriteauthor( cls , data ):
        query = "INSERT INTO favorites ( author_id, book_id ) VALUES (%(author_id)s, %(book_id)s );"
        return connectToMySQL('books').query_db( query, data )