from app import db
from app.models.computers import Computer


# ── CREATE ────────────────────────────────────────────────────────────────────

def test_create_computer(computer):
    """El fixture crea el equipo; verificar atributos y valores por defecto."""
    assert computer.idComputer is not None
    assert computer.brandComputer == "Lenovo Fixture"
    assert computer.modelComputer == "ThinkPad Fixture"
    assert computer.statusComputer == "Active"
    assert computer.computerLoans == []


# ── READ ──────────────────────────────────────────────────────────────────────

def test_read_computer_by_id(computer):
    """Leer un equipo de la BD por su clave primaria."""
    fetched = db.session.get(Computer, computer.idComputer)
    assert fetched is not None
    assert fetched.brandComputer == computer.brandComputer
    assert fetched.modelComputer == computer.modelComputer


def test_read_computer_filter(app):
    """Filtrar equipos por marca mediante query."""
    c1 = Computer(brandComputer="Dell", modelComputer="OptiPlex 3080")
    c2 = Computer(brandComputer="Dell", modelComputer="Latitude 5420")
    db.session.add_all([c1, c2])
    db.session.commit()

    results = Computer.query.filter_by(brandComputer="Dell").all()
    assert len(results) >= 2


def test_computer_repr(computer):
    """Verificar la representación __repr__ del modelo."""
    assert repr(computer) == (
        f"<Computer {computer.idComputer} - "
        f"{computer.brandComputer} {computer.modelComputer}>"
    )


# ── UPDATE ────────────────────────────────────────────────────────────────────

def test_update_computer(computer):
    """Actualizar marca, modelo y estado de un equipo existente."""
    computer.brandComputer = "Asus (updated)"
    computer.modelComputer = "ZenBook 14"
    computer.statusComputer = "Maintenance"
    db.session.commit()

    updated = db.session.get(Computer, computer.idComputer)
    assert updated.brandComputer == "Asus (updated)"
    assert updated.modelComputer == "ZenBook 14"
    assert updated.statusComputer == "Maintenance"


# ── DELETE ────────────────────────────────────────────────────────────────────

def test_delete_computer(computer):
    """Eliminar un equipo y verificar que ya no existe en la BD."""
    computer_id = computer.idComputer
    db.session.delete(computer)
    db.session.commit()

    deleted = db.session.get(Computer, computer_id)
    assert deleted is None


# ── ROUTE CRUD ────────────────────────────────────────────────────────────────

def test_route_computers_index(client):
    """GET /computers/ devuelve 200."""
    response = client.get('/computers/')
    assert response.status_code == 200


def test_route_computers_add(client):
    """POST /computers/add crea un nuevo equipo y redirige."""
    response = client.post('/computers/add', data={
        'brandComputer': 'Samsung',
        'modelComputer': 'Galaxy Book',
        'statusComputer': 'Active'
    }, follow_redirects=True)
    assert response.status_code == 200

    created = Computer.query.filter_by(brandComputer='Samsung').first()
    assert created is not None
    assert created.modelComputer == 'Galaxy Book'


def test_route_computers_update(client, computer):
    """POST /computers/update/<id> actualiza los datos del equipo."""
    response = client.post(f'/computers/update/{computer.idComputer}', data={
        'brandComputer': 'MSI Updated',
        'modelComputer': 'Creator Pro',
        'statusComputer': 'Inactive'
    }, follow_redirects=True)
    assert response.status_code == 200

    updated = db.session.get(Computer, computer.idComputer)
    assert updated.brandComputer == 'MSI Updated'
    assert updated.modelComputer == 'Creator Pro'
    assert updated.statusComputer == 'Inactive'


def test_route_computers_delete(client, computer):
    """POST /computers/delete/<id> elimina el equipo de la BD."""
    computer_id = computer.idComputer
    response = client.post(f'/computers/delete/{computer_id}', follow_redirects=True)
    assert response.status_code == 200

    deleted = db.session.get(Computer, computer_id)
    assert deleted is None
