from app import create_app, db
import pytest


# ── INFRAESTRUCTURA ───────────────────────────────────────────────────────────

@pytest.fixture
def app():
    """Crea la aplicación Flask con BD SQLite en memoria para cada test."""
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Cliente HTTP de prueba de Flask."""
    return app.test_client()


# ── FIXTURES DE ENTIDADES ─────────────────────────────────────────────────────

@pytest.fixture
def user(app):
    """Usuario genérico persitido en BD, disponible en toda la sesión de test."""
    from app.models.users import User
    user = User(nameUser="test_user", passwordUser="test_password")
    db.session.add(user)
    db.session.commit()
    yield user


@pytest.fixture
def author(app):
    """Autor genérico persistido en BD."""
    from app.models.authors import Author
    author = Author(nameAuthor="Autor Fixture", nationalityAuthor="Colombiano")
    db.session.add(author)
    db.session.commit()
    yield author


@pytest.fixture
def book(app, author):
    """Libro genérico persistido en BD, asociado al fixture author."""
    from app.models.books import Book
    book = Book(titleBook="Libro Fixture", author=author)
    db.session.add(book)
    db.session.commit()
    yield book


@pytest.fixture
def computer(app):
    """Equipo de cómputo genérico persistido en BD."""
    from app.models.computers import Computer
    computer = Computer(brandComputer="Lenovo Fixture", modelComputer="ThinkPad Fixture")
    db.session.add(computer)
    db.session.commit()
    yield computer


@pytest.fixture
def room(app):
    """Sala genérica persistida en BD."""
    from app.models.rooms import Room
    room = Room(name="Sala Fixture", description="Sala de prueba fixture")
    db.session.add(room)
    db.session.commit()
    yield room


@pytest.fixture
def loan(app, user, book):
    """Préstamo de libro activo persistido en BD."""
    from app.models.loans import Loan
    loan = Loan(book=book, user=user)
    db.session.add(loan)
    db.session.commit()
    yield loan


@pytest.fixture
def computer_loan(app, user, computer):
    """Préstamo de equipo activo persistido en BD."""
    from app.models.cloans import ComputerLoan
    cloan = ComputerLoan(computer=computer, user=user)
    db.session.add(cloan)
    db.session.commit()
    yield cloan