from app import db
from app.models.rooms import Room


def test_create_room(app):
    room = Room(name="Sala A", description="Sala de estudio grupal")
    db.session.add(room)
    db.session.commit()
    assert room.id is not None
    assert room.name == "Sala A"
    assert room.description == "Sala de estudio grupal"


def test_room_repr(app):
    room = Room(name="Sala B", description="Sala audiovisual")
    db.session.add(room)
    db.session.commit()
    assert repr(room) == f"<Room {room.id} - Sala B>"
