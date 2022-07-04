from flask import Flask, render_template, redirect, request, session, url_for

from flask_app.models.author import Author
from flask_app.models.book import Book

from flask_app import app

@app.route('/authors')
def author_list():
    authors = Author.get_all()
    return render_template('author.html', authors = authors)

@app.route('/addauthor', methods = ["post"])
def addauthor():
    data = {
        "name": request.form["name"],
    }
    Author.save(data)
    return redirect("/authors")

@app.route('/authors/<int:id>')
def showauthor(id):
    data = {
        "id": id
    }
    session["id"] = id
    books = Book.get_all()
    author = Author.get_authors_books(data)
    return render_template('authorid.html', author = author, books = books)

@app.route('/addbook', methods = ["post"])
def addbook():
    data = {
        "author_id": session["id"],
        "book_id": request.form["title"]
    }
    Author.addfavorite(data)
    return redirect(url_for('showauthor', id = data['author_id']))

