from app import db
from app.models.authors import Author
from app.models.books import Book


def test_create_book(app):
    author = Author(nameAuthor="Mario Vargas Llosa", nationalityAuthor="Peruano")
    db.session.add(author)
    db.session.commit()
    book = Book(titleBook="La ciudad y los perros", author=author)
    db.session.add(book)
    db.session.commit()
    assert book.idBook is not None
    assert book.titleBook == "La ciudad y los perros"
    assert book.authorId == author.idAuthor
    assert book.author == author


def test_book_repr(app):
    book = Book(titleBook="El tunel")
    db.session.add(book)
    db.session.commit()
    assert repr(book) == "<Book El tunel>"


def test_book_loans_relationship(app):
    book = Book(titleBook="Ficciones")
    db.session.add(book)
    db.session.commit()
    assert book.loans.all() == []
