from app import db
from app.models.rooms import Room


# ── CREATE ────────────────────────────────────────────────────────────────────

def test_create_room(room):
    """El fixture crea la sala; verificar sus atributos."""
    assert room.id is not None
    assert room.name == "Sala Fixture"
    assert room.description == "Sala de prueba fixture"


# ── READ ──────────────────────────────────────────────────────────────────────

def test_read_room_by_id(room):
    """Consultar una sala por su clave primaria."""
    fetched = db.session.get(Room, room.id)
    assert fetched is not None
    assert fetched.name == room.name
    assert fetched.description == room.description


def test_read_room_filter(room):
    """Filtrar salas por nombre mediante query."""
    results = Room.query.filter_by(name=room.name).all()
    assert len(results) >= 1
    assert results[0].id == room.id


def test_room_repr(room):
    """Verificar la representación __repr__ del modelo."""
    assert repr(room) == f"<Room {room.id} - {room.name}>"


# ── UPDATE ────────────────────────────────────────────────────────────────────

def test_update_room(room):
    """Actualizar nombre y descripción de una sala existente."""
    room.name = "Sala Actualizada"
    room.description = "Descripcion actualizada"
    db.session.commit()

    updated = db.session.get(Room, room.id)
    assert updated.name == "Sala Actualizada"
    assert updated.description == "Descripcion actualizada"


# ── DELETE ────────────────────────────────────────────────────────────────────

def test_delete_room(room):
    """Eliminar una sala y verificar que ya no existe en la BD."""
    room_id = room.id
    db.session.delete(room)
    db.session.commit()

    deleted = db.session.get(Room, room_id)
    assert deleted is None


# ── ROUTE CRUD ────────────────────────────────────────────────────────────────

def test_route_rooms_index(client):
    """GET /room/ devuelve 200."""
    response = client.get('/room/')
    assert response.status_code == 200


def test_route_rooms_add(client):
    """POST /room/add crea una nueva sala y redirige al índice."""
    response = client.post('/room/add', data={
        'name': 'Sala Ruta Add',
        'description': 'Creada desde ruta'
    }, follow_redirects=True)
    assert response.status_code == 200

    created = Room.query.filter_by(name='Sala Ruta Add').first()
    assert created is not None
    assert created.description == 'Creada desde ruta'


def test_route_rooms_edit(client, room):
    """POST /room/edit/<id> actualiza los datos de la sala."""
    response = client.post(f'/room/edit/{room.id}', data={
        'name': 'Sala Ruta Editada',
        'description': 'Despues del edit'
    }, follow_redirects=True)
    assert response.status_code == 200

    updated = db.session.get(Room, room.id)
    assert updated.name == 'Sala Ruta Editada'
    assert updated.description == 'Despues del edit'


def test_route_rooms_delete(client, room):
    """GET /room/delete/<id> elimina la sala de la BD."""
    room_id = room.id
    response = client.get(f'/room/delete/{room_id}', follow_redirects=True)
    assert response.status_code == 200

    deleted = db.session.get(Room, room_id)
    assert deleted is None
