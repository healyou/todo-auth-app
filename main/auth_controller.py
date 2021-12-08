# flask imports
from flask import Flask
from .blueprint.auth_blueprint import auth
# TODO main наверное не должен быть пакетом


def create_app(app):
    app.register_blueprint(auth, url_prefix='/auth')
    return app


if __name__ == "__main__":
    flask_app = Flask(__name__)
    create_app(flask_app)
    flask_app.run(debug=True, host='0.0.0.0', port=8887)
