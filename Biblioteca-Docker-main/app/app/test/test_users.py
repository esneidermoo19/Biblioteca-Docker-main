from app import db
from app.models.users import User


# ── READ ──────────────────────────────────────────────────────────────────────

def test_index(client):
    """GET /User/ devuelve 200 y muestra la sección de usuarios."""
    response = client.get('/User/')
    assert response.status_code == 200
    assert b"Usuarios" in response.data


def test_detail_user(client, user):
    """GET /User/detail/<id> devuelve 200 y muestra el detalle del usuario."""
    response = client.get(f'/User/detail/{user.idUser}', follow_redirects=True)
    assert response.status_code == 200


def test_user_qr_route(client, user):
    """GET /User/qr/<id> devuelve 200 y un PNG del código QR."""
    response = client.get(f'/User/qr/{user.idUser}')
    assert response.status_code == 200
    assert response.content_type == 'image/png'


# ── CREATE ────────────────────────────────────────────────────────────────────

def test_add_user(client):
    """POST /User/add crea un nuevo usuario y lo persiste en la BD."""
    response = client.post('/User/add', data={
        'nameUser': 'new_user_ruta',
        'passwordUser': 'new_password'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Usuarios" in response.data

    created = User.query.filter_by(nameUser='new_user_ruta').first()
    assert created is not None
    assert created.passwordUser == 'new_password'


# ── UPDATE ────────────────────────────────────────────────────────────────────

def test_edit_user(client, user):
    """POST /User/edit/<id> actualiza el usuario y persiste los cambios en BD."""
    response = client.post(f'/User/edit/{user.idUser}', data={
        'nameUser': 'updated_user',
        'passwordUser': 'updated_password'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"updated_user" in response.data

    updated = db.session.get(User, user.idUser)
    assert updated.nameUser == 'updated_user'
    assert updated.passwordUser == 'updated_password'


# ── DELETE ────────────────────────────────────────────────────────────────────

def test_delete_user(client, user):
    """GET /User/delete/<id> elimina al usuario de la BD."""
    user_id = user.idUser
    response = client.get(f'/User/delete/{user_id}', follow_redirects=True)
    assert response.status_code == 200
    assert b"Usuarios" in response.data

    deleted = db.session.get(User, user_id)
    assert deleted is None
