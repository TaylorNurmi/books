from flask import Flask, render_template, redirect, request, session, url_for

from flask_app.models.author import Author
from flask_app.models.book import Book

from flask_app import app

@app.route('/books')
def book_list():
    books =   Book.get_all()
    return render_template('book.html', books = books)

@app.route('/addtobooks', methods = ["post"])
def addtobooks():
    data = {
        "title": request.form["title"],
        "pages": request.form["pages"]
    }
    Book.save(data)
    return redirect("/books")

@app.route('/books/<int:id>')
def showbook(id):
    data = {
        "id": id
    }
    session["id"] = id
    authors = Author.get_all()
    book = Book.get_books_author(data)
    return render_template('bookid.html', authors = authors, book = book)

@app.route('/addfav', methods = ["post"])
def addauthorfav():
    data = {
        "book_id": session["id"],
        "author_id": request.form["name"]
    }
    Book.addfavoriteauthor(data)
    return redirect(url_for('showbook', id = data['book_id']))
