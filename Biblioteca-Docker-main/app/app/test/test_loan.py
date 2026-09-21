from datetime import datetime, timedelta
from app import db
from app.models.books import Book
from app.models.loans import Loan


# ── CREATE ────────────────────────────────────────────────────────────────────

def test_create_loan(loan, book, user):
    """El fixture crea el préstamo; verificar todos sus atributos y relaciones."""
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


# ── READ ──────────────────────────────────────────────────────────────────────

def test_read_loan_by_id(loan):
    """Consultar un préstamo de libro por su clave primaria."""
    fetched = db.session.get(Loan, loan.idLoan)
    assert fetched is not None
    assert fetched.status == "Active"
    assert fetched.bookId == loan.bookId
    assert fetched.userId == loan.userId


def test_read_loan_relationships(loan, book, user):
    """Verificar que las relaciones book/user del préstamo se resuelven correctamente."""
    assert loan.book.titleBook == book.titleBook
    assert loan.user.idUser == user.idUser


def test_loan_repr(loan, book, user):
    """Verificar la representación __repr__ del modelo."""
    assert repr(loan) == (
        f"<Loan {loan.idLoan} of Book {book.idBook} to User {user.idUser}>"
    )


# ── UPDATE ────────────────────────────────────────────────────────────────────

def test_update_loan_status_and_fine(loan):
    """Actualizar estado, fecha de devolución y multa de un préstamo existente."""
    loan.status = "Returned"
    loan.returnDate = datetime.now()
    loan.fine = 5.0
    db.session.commit()

    updated = db.session.get(Loan, loan.idLoan)
    assert updated.status == "Returned"
    assert updated.returnDate is not None
    assert updated.fine == 5.0


# ── DELETE ────────────────────────────────────────────────────────────────────

def test_delete_loan(loan):
    """Eliminar un préstamo y verificar que ya no existe en la BD."""
    loan_id = loan.idLoan
    db.session.delete(loan)
    db.session.commit()

    deleted = db.session.get(Loan, loan_id)
    assert deleted is None


# ── ROUTE CRUD ────────────────────────────────────────────────────────────────

def test_route_loans_index(client):
    """GET /Loan/ devuelve 200."""
    response = client.get('/Loan/')
    assert response.status_code == 200


def test_route_loans_add(client, book, user):
    """POST /Loan/add crea un nuevo préstamo y lo persiste en la BD."""
    response = client.post('/Loan/add', data={
        'bookId': book.idBook,
        'userId': user.idUser
    }, follow_redirects=True)
    assert response.status_code == 200

    created = Loan.query.filter_by(bookId=book.idBook, userId=user.idUser).first()
    assert created is not None
    assert created.status == 'Active'


def test_route_loans_edit(client, loan):
    """POST /Loan/edit/<id> actualiza estado, multa y fecha de devolución."""
    future_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
    response = client.post(f'/Loan/edit/{loan.idLoan}', data={
        'returnDate': future_date,
        'fine': '0.0',
        'status': 'Active'
    }, follow_redirects=True)
    assert response.status_code == 200

    updated = db.session.get(Loan, loan.idLoan)
    assert updated.fine == 0.0
    assert updated.status == 'Active'


def test_route_loans_delete(client, loan):
    """GET /Loan/delete/<id> elimina el préstamo de la BD."""
    loan_id = loan.idLoan
    response = client.get(f'/Loan/delete/{loan_id}', follow_redirects=True)
    assert response.status_code == 200

    deleted = db.session.get(Loan, loan_id)
    assert deleted is None


def test_route_loans_return(client, loan, book, user):
    """GET /Loan/return/<id> marca el préstamo como Returned."""
    # Establecer returnDate en el pasado para disparar multa
    loan.returnDate = datetime.now() - timedelta(days=3)
    db.session.commit()

    response = client.get(f'/Loan/return/{loan.idLoan}', follow_redirects=True)
    assert response.status_code == 200

    returned = db.session.get(Loan, loan.idLoan)
    assert returned.status == 'Returned'
