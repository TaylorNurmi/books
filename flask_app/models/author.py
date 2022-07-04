from flask_app.config.mysqlconnection import connectToMySQL


from flask_app.models import book



class Author:

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.books = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM authors;"
        results = connectToMySQL('books').query_db(query)
        authors = []
        for author in results:
            authors.append( cls(author) )
        return authors

    @classmethod
    def save( cls , data ):
        query = "INSERT INTO authors ( name, created_at , updated_at ) VALUES (%(name)s, NOW(),NOW() );"
        return connectToMySQL('books').query_db( query, data )


    @classmethod
    def get_authors_books( cls , data ):
        query = "SELECT * FROM authors LEFT JOIN favorites ON favorites.author_id = authors.id LEFT JOIN books ON favorites.book_id = books.id WHERE authors.id = %(id)s;"
        results = connectToMySQL('books').query_db( query , data ) 
        author = cls( results[0] )
        for row in results:
            book_data = {
                "id" : row["books.id"],
                "title" : row["title"],
                "pages" : row["pages"],
                "created_at" : row["books.created_at"],
                "updated_at" : row["books.updated_at"]
            }
            author.books.append( book.Book( book_data ) )
        return author

    @classmethod
    def addfavorite( cls , data ):
        query = "INSERT INTO favorites ( author_id, book_id ) VALUES (%(author_id)s, %(book_id)s );"
        return connectToMySQL('books').query_db( query, data )