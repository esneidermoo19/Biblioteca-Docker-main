from datetime import datetime
from app import db
from app.models.cloans import ComputerLoan
from app.models.computers import Computer


# ── CREATE ────────────────────────────────────────────────────────────────────

def test_create_computer_loan(computer_loan, computer, user):
    """El fixture crea el préstamo de equipo; verificar atributos y relaciones."""
    assert computer_loan.idLoan is not None
    assert computer_loan.status == "Active"
    assert computer_loan.loanDate is not None
    assert computer_loan.returnDate is None
    assert computer_loan.computerId == computer.idComputer
    assert computer_loan.userId == user.idUser
    assert computer_loan.computer == computer
    assert computer_loan.user == user
    assert computer_loan in computer.computerLoans
    assert computer_loan in user.computerLoansUser.all()


# ── READ ──────────────────────────────────────────────────────────────────────

def test_read_computer_loan_by_id(computer_loan):
    """Consultar un préstamo de equipo por su clave primaria."""
    fetched = db.session.get(ComputerLoan, computer_loan.idLoan)
    assert fetched is not None
    assert fetched.computerId == computer_loan.computerId
    assert fetched.userId == computer_loan.userId
    assert fetched.status == "Active"


def test_read_computer_loan_relationships(computer_loan, computer, user):
    """Verificar que las relaciones computer/user del préstamo se resuelven."""
    assert computer_loan.computer.brandComputer == computer.brandComputer
    assert computer_loan.user.idUser == user.idUser


def test_computer_loan_repr(computer_loan, computer, user):
    """Verificar la representación __repr__ del modelo."""
    assert repr(computer_loan) == (
        f"<ComputerLoan {computer_loan.idLoan} of Computer "
        f"{computer.idComputer} to User {user.idUser}>"
    )


# ── UPDATE ────────────────────────────────────────────────────────────────────

def test_update_computer_loan_status(computer_loan):
    """Actualizar estado y fecha de devolución de un préstamo de equipo."""
    computer_loan.status = "Returned"
    computer_loan.returnDate = datetime.now()
    db.session.commit()

    updated = db.session.get(ComputerLoan, computer_loan.idLoan)
    assert updated.status == "Returned"
    assert updated.returnDate is not None


# ── DELETE ────────────────────────────────────────────────────────────────────

def test_delete_computer_loan(computer_loan):
    """Eliminar un préstamo de equipo y verificar que ya no existe en la BD."""
    cloan_id = computer_loan.idLoan
    db.session.delete(computer_loan)
    db.session.commit()

    deleted = db.session.get(ComputerLoan, cloan_id)
    assert deleted is None


# ── ROUTE CRUD ────────────────────────────────────────────────────────────────

def test_route_cloans_index(client):
    """GET /cloans/ devuelve 200."""
    response = client.get('/cloans/')
    assert response.status_code == 200


def test_route_cloans_add(client, computer, user):
    """POST /cloans/add crea un nuevo préstamo de equipo y lo persiste en BD."""
    response = client.post('/cloans/add', data={
        'computerId': computer.idComputer,
        'userId': user.idUser,
        'status': 'Active'
    }, follow_redirects=True)
    assert response.status_code == 200

    created = ComputerLoan.query.filter_by(
        computerId=computer.idComputer, userId=user.idUser
    ).first()
    assert created is not None
    assert created.status == 'Active'


def test_route_cloans_update(client, computer_loan, computer, user):
    """POST /cloans/update/<id> actualiza el estado del préstamo de equipo vía ruta."""
    loan_date_str = (
        computer_loan.loanDate.strftime('%Y-%m-%d') if computer_loan.loanDate else ''
    )
    response = client.post(f'/cloans/update/{computer_loan.idLoan}', data={
        'computerId': computer.idComputer,
        'userId': user.idUser,
        'loanDate': loan_date_str,
        'returnDate': '',
        'status': 'Returned'
    }, follow_redirects=True)
    assert response.status_code == 200

    updated = db.session.get(ComputerLoan, computer_loan.idLoan)
    assert updated.status == 'Returned'


def test_route_cloans_delete(client, computer_loan):
    """POST /cloans/delete/<id> elimina el préstamo de equipo de la BD."""
    cloan_id = computer_loan.idLoan
    response = client.post(f'/cloans/delete/{cloan_id}', follow_redirects=True)
    assert response.status_code == 200

    deleted = db.session.get(ComputerLoan, cloan_id)
    assert deleted is None


def test_route_cloans_return(client, computer_loan):
    """POST /cloans/return/<id> marca el préstamo de equipo como Returned."""
    response = client.post(
        f'/cloans/return/{computer_loan.idLoan}', follow_redirects=True
    )
    assert response.status_code == 200

    returned = db.session.get(ComputerLoan, computer_loan.idLoan)
    assert returned.status == 'Returned'
    assert returned.returnDate is not None
