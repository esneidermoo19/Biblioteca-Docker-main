from app import db
from app.models.authors import Author
from app.models.books import Book


def test_create_author(app):
    author = Author(nameAuthor="Gabriel Garcia Marquez", nationalityAuthor="Colombiano")
    db.session.add(author)
    db.session.commit()
    assert author.idAuthor is not None
    assert author.nameAuthor == "Gabriel Garcia Marquez"
    assert author.nationalityAuthor == "Colombiano"


def test_author_repr(app):
    author = Author(nameAuthor="Jorge Luis Borges", nationalityAuthor="Argentino")
    db.session.add(author)
    db.session.commit()
    assert repr(author) == "<Author Jorge Luis Borges>"


def test_author_books_relationship(app):
    author = Author(nameAuthor="Julio Cortazar", nationalityAuthor="Argentino")
    db.session.add(author)
    db.session.commit()
    book1 = Book(titleBook="Rayuela", author=author)
    book2 = Book(titleBook="Bestiario", author=author)
    db.session.add_all([book1, book2])
    db.session.commit()
    assert author.books.count() == 2
    assert book1 in author.books.all()
    assert book2 in author.books.all()
