from app import db
from app.models.users import User


def test_create_user(app):
    user = User(nameUser="lector_uno", passwordUser="secreto123")
    db.session.add(user)
    db.session.commit()
    assert user.idUser is not None
    assert user.nameUser == "lector_uno"
    assert user.passwordUser == "secreto123"


def test_user_get_id(user):
    assert user.get_id() == str(user.idUser)


def test_user_generate_qr(app, user):
    qr_code = user.generate_qr()
    assert isinstance(qr_code, str)
    assert len(qr_code) > 0


def test_user_empty_loans(user):
    assert user.loansUser.all() == []
    assert user.computerLoansUser.all() == []
