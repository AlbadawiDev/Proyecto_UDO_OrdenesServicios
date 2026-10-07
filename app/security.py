"""Protección de formularios sin dependencias adicionales."""
import hmac
import secrets
from flask import abort, request, session


def register_security(app):
    def csrf_token():
        if '_csrf' not in session:
            session['_csrf'] = secrets.token_urlsafe(32)
        return session['_csrf']

    app.jinja_env.globals['csrf_token'] = csrf_token

    @app.before_request
    def protect_mutations():
        if request.method not in ('GET', 'HEAD', 'OPTIONS'):
            expected = session.get('_csrf', '')
            supplied = request.form.get('_csrf') or request.headers.get('X-CSRF-Token', '')
            if not expected or not hmac.compare_digest(expected.encode(), supplied.encode()):
                abort(403, description='Formulario vencido o inválido. Recarga la página e inténtalo nuevamente.')

    @app.after_request
    def response_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['Referrer-Policy'] = 'same-origin'
        response.headers['Cache-Control'] = 'no-store'
        return response
