from app import db
from app.models.users import User


# ── CREATE ────────────────────────────────────────────────────────────────────

def test_create_user(app):
    """Crear un usuario independiente y verificar que se persiste correctamente."""
    new_user = User(nameUser="lector_uno", passwordUser="secreto123")
    db.session.add(new_user)
    db.session.commit()
    assert new_user.idUser is not None
    assert new_user.nameUser == "lector_uno"
    assert new_user.passwordUser == "secreto123"


# ── READ ──────────────────────────────────────────────────────────────────────

def test_read_user_by_id(user):
    """Consultar un usuario por su clave primaria."""
    fetched = db.session.get(User, user.idUser)
    assert fetched is not None
    assert fetched.nameUser == user.nameUser
    assert fetched.passwordUser == user.passwordUser


def test_read_user_filter(user):
    """Filtrar usuarios por nombre de usuario."""
    results = User.query.filter_by(nameUser=user.nameUser).all()
    assert len(results) == 1
    assert results[0].idUser == user.idUser


# ── UPDATE ────────────────────────────────────────────────────────────────────

def test_update_user(user):
    """Actualizar nombre y contraseña de un usuario existente."""
    user.nameUser = "lector_upd_2"
    user.passwordUser = "despues"
    db.session.commit()

    updated = db.session.get(User, user.idUser)
    assert updated.nameUser == "lector_upd_2"
    assert updated.passwordUser == "despues"


# ── DELETE ────────────────────────────────────────────────────────────────────

def test_delete_user_model(user):
    """Eliminar un usuario de la BD y verificar su ausencia."""
    user_id = user.idUser
    db.session.delete(user)
    db.session.commit()

    deleted = db.session.get(User, user_id)
    assert deleted is None


# ── FUNCIONALES ───────────────────────────────────────────────────────────────

def test_user_get_id(user):
    """get_id() devuelve el ID del usuario como string."""
    assert user.get_id() == str(user.idUser)


def test_user_generate_qr(user):
    """generate_qr() devuelve una cadena base64 no vacía."""
    qr_code = user.generate_qr()
    assert isinstance(qr_code, str)
    assert len(qr_code) > 0


def test_user_empty_loans(user):
    """Un usuario recién creado no tiene préstamos ni préstamos de equipos."""
    assert user.loansUser.all() == []
    assert user.computerLoansUser.all() == []
