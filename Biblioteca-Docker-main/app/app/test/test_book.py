from app import db
from app.models.authors import Author
from app.models.books import Book


# ── CREATE ────────────────────────────────────────────────────────────────────

def test_create_book(book, author):
    """El fixture crea el libro; verificar atributos y relación con autor."""
    assert book.idBook is not None
    assert book.titleBook == "Libro Fixture"
    assert book.authorId == author.idAuthor
    assert book.author == author


# ── READ ──────────────────────────────────────────────────────────────────────

def test_read_book_by_id(book):
    """Consultar un libro por su clave primaria."""
    fetched = db.session.get(Book, book.idBook)
    assert fetched is not None
    assert fetched.titleBook == book.titleBook


def test_read_book_filter(book):
    """Filtrar libros por título mediante query."""
    results = Book.query.filter_by(titleBook=book.titleBook).all()
    assert len(results) >= 1
    assert results[0].idBook == book.idBook


def test_book_repr(book):
    """Verificar la representación __repr__ del modelo."""
    assert repr(book) == f"<Book {book.titleBook}>"


def test_book_loans_relationship(book):
    """Un libro recién creado no tiene préstamos activos."""
    assert book.loans.all() == []


# ── UPDATE ────────────────────────────────────────────────────────────────────

def test_update_book(book, author):
    """Actualizar el título de un libro existente."""
    book.titleBook = "Titulo Actualizado"
    db.session.commit()

    updated = db.session.get(Book, book.idBook)
    assert updated.titleBook == "Titulo Actualizado"
    assert updated.authorId == author.idAuthor


# ── DELETE ────────────────────────────────────────────────────────────────────

def test_delete_book(book):
    """Eliminar un libro y verificar que ya no existe en la BD."""
    book_id = book.idBook
    db.session.delete(book)
    db.session.commit()

    deleted = db.session.get(Book, book_id)
    assert deleted is None


# ── ROUTE CRUD ────────────────────────────────────────────────────────────────

def test_route_books_index(client):
    """GET /Book/ devuelve 200."""
    response = client.get('/Book/')
    assert response.status_code == 200


def test_route_books_add(client, author):
    """POST /Book/add crea un nuevo libro y redirige al índice."""
    response = client.post('/Book/add', data={
        'titleBook': 'Libro Ruta Add',
        'authorId': author.idAuthor
    }, follow_redirects=True)
    assert response.status_code == 200

    created = Book.query.filter_by(titleBook='Libro Ruta Add').first()
    assert created is not None
    assert created.authorId == author.idAuthor


def test_route_books_edit(client, book, author):
    """POST /Book/edit/<id> actualiza los datos del libro."""
    response = client.post(f'/Book/edit/{book.idBook}', data={
        'titleBook': 'Libro Ruta Edit Actualizado',
        'authorId': author.idAuthor
    }, follow_redirects=True)
    assert response.status_code == 200

    updated = db.session.get(Book, book.idBook)
    assert updated.titleBook == 'Libro Ruta Edit Actualizado'


def test_route_books_delete(client, book):
    """GET /Book/delete/<id> elimina el libro de la BD."""
    book_id = book.idBook
    response = client.get(f'/Book/delete/{book_id}', follow_redirects=True)
    assert response.status_code == 200

    deleted = db.session.get(Book, book_id)
    assert deleted is None
