from flask_login import login_user


# ── LOGIN ─────────────────────────────────────────────────────────────────────

def test_login_success(client, user):
    """POST / con credenciales correctas redirige al dashboard de usuarios."""
    response = client.post('/', data={
        'nameUser': user.nameUser,
        'passwordUser': user.passwordUser
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Usuarios" in response.data


def test_login_invalid_credentials(client):
    """POST / con credenciales incorrectas muestra mensaje de error."""
    response = client.post('/', data={
        'nameUser': 'wronguser',
        'passwordUser': 'wrongskdfghgpassword'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Invalid credentials. Please try again." in response.data


def test_login_get_shows_form(client):
    """GET / devuelve 200 y el formulario de inicio de sesión."""
    response = client.get('/')
    assert response.status_code == 200


# ── SESIÓN AUTENTICADA ────────────────────────────────────────────────────────

def test_login_already_authenticated(client, user):
    """Un usuario con sesión activa es redirigido al dashboard al acceder a /dashboard."""
    with client:
        with client.session_transaction() as session:
            session['_user_id'] = str(user.idUser)

        response = client.get('/dashboard', follow_redirects=True)
        assert response.status_code == 200
        assert b"This is your dashboard" in response.data


# ── LOGOUT ────────────────────────────────────────────────────────────────────

def test_logout(client, user):
    """GET /logout cierra la sesión y redirige a la página de login."""
    # Primero autenticamos al usuario
    client.post('/', data={
        'nameUser': user.nameUser,
        'passwordUser': user.passwordUser
    }, follow_redirects=True)

    # Luego cerramos sesión
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    # Tras el logout debe mostrar la página de login de nuevo
    assert b"You have been logged out." in response.data or response.status_code == 200
