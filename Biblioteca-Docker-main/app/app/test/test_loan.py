from datetime import datetime
from app import db
from app.models.authors import Author
from app.models.books import Book
from app.models.loans import Loan


def test_create_loan(app, user):
    author = Author(nameAuthor="Miguel de Cervantes", nationalityAuthor="Espanol")
    book = Book(titleBook="Don Quijote", author=author)
    db.session.add_all([author, book])
    db.session.commit()
    loan = Loan(book=book, user=user)
    db.session.add(loan)
    db.session.commit()
    assert loan.idLoan is not None
    assert loan.status == "Active"
    assert loan.fine == 0.0
    assert loan.loanDate is not None
    assert loan.returnDate is None
    assert loan.bookId == book.idBook
    assert loan.userId == user.idUser
    assert loan.book == book
    assert loan.user == user
    assert loan in user.loansUser.all()
    assert loan in book.loans.all()


def test_loan_repr(app, user):
    book = Book(titleBook="La Galatea")
    db.session.add(book)
    db.session.commit()
    loan = Loan(book=book, user=user)
    db.session.add(loan)
    db.session.commit()
    assert repr(loan) == f"<Loan {loan.idLoan} of Book {book.idBook} to User {user.idUser}>"


def test_loan_update_status_and_fine(app, user):
    book = Book(titleBook="Novelas ejemplares")
    db.session.add(book)
    db.session.commit()
    loan = Loan(book=book, user=user)
    db.session.add(loan)
    db.session.commit()
    loan.status = "Returned"
    loan.returnDate = datetime.now()
    loan.fine = 5.0
    db.session.commit()
    assert loan.status == "Returned"
    assert loan.returnDate is not None
    assert loan.fine == 5.0
