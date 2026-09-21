from app import db
from app.models.authors import Author
from app.models.books import Book


# ── CREATE ────────────────────────────────────────────────────────────────────

def test_create_author(author):
    """El fixture crea el autor; verificar que se persiste correctamente."""
    assert author.idAuthor is not None
    assert author.nameAuthor == "Autor Fixture"
    assert author.nationalityAuthor == "Colombiano"


# ── READ ──────────────────────────────────────────────────────────────────────

def test_read_author_by_id(author):
    """Consultar un autor por su clave primaria."""
    fetched = db.session.get(Author, author.idAuthor)
    assert fetched is not None
    assert fetched.nameAuthor == author.nameAuthor
    assert fetched.nationalityAuthor == author.nationalityAuthor


def test_read_author_filter(author):
    """Filtrar autores por nombre mediante query."""
    results = Author.query.filter_by(nameAuthor=author.nameAuthor).all()
    assert len(results) >= 1
    assert results[0].idAuthor == author.idAuthor


def test_author_repr(author):
    """Verificar la representación __repr__ del modelo."""
    assert repr(author) == f"<Author {author.nameAuthor}>"


def test_author_books_relationship(author):
    """Un autor puede tener múltiples libros asociados."""
    book1 = Book(titleBook="Rayuela", author=author)
    book2 = Book(titleBook="Bestiario", author=author)
    db.session.add_all([book1, book2])
    db.session.commit()
    assert author.books.count() == 2
    assert book1 in author.books.all()
    assert book2 in author.books.all()


# ── UPDATE ────────────────────────────────────────────────────────────────────

def test_update_author(author):
    """Actualizar nombre y nacionalidad de un autor existente."""
    author.nameAuthor = "Autor Actualizado"
    author.nationalityAuthor = "Mexicano"
    db.session.commit()

    updated = db.session.get(Author, author.idAuthor)
    assert updated.nameAuthor == "Autor Actualizado"
    assert updated.nationalityAuthor == "Mexicano"


# ── DELETE ────────────────────────────────────────────────────────────────────

def test_delete_author(author):
    """Eliminar un autor y verificar que ya no existe en la BD."""
    author_id = author.idAuthor
    db.session.delete(author)
    db.session.commit()

    deleted = db.session.get(Author, author_id)
    assert deleted is None


# ── ROUTE CRUD ────────────────────────────────────────────────────────────────

def test_route_authors_index(client):
    """GET /Author/ devuelve 200."""
    response = client.get('/Author/')
    assert response.status_code == 200


def test_route_authors_add(client):
    """POST /Author/add crea un nuevo autor y redirige al índice."""
    response = client.post('/Author/add', data={
        'nameAuthor': 'Isabel Allende',
        'nationalityAuthor': 'Chilena'
    }, follow_redirects=True)
    assert response.status_code == 200

    created = Author.query.filter_by(nameAuthor='Isabel Allende').first()
    assert created is not None
    assert created.nationalityAuthor == 'Chilena'


def test_route_authors_edit(client, author):
    """POST /Author/edit/<id> actualiza los datos del autor."""
    response = client.post(f'/Author/edit/{author.idAuthor}', data={
        'nameAuthor': 'Autor Ruta Editado',
        'nationalityAuthor': 'Venezolano'
    }, follow_redirects=True)
    assert response.status_code == 200

    updated = db.session.get(Author, author.idAuthor)
    assert updated.nameAuthor == 'Autor Ruta Editado'
    assert updated.nationalityAuthor == 'Venezolano'


def test_route_authors_delete(client, author):
    """GET /Author/delete/<id> elimina el autor de la BD."""
    author_id = author.idAuthor
    response = client.get(f'/Author/delete/{author_id}', follow_redirects=True)
    assert response.status_code == 200

    deleted = db.session.get(Author, author_id)
    assert deleted is None
