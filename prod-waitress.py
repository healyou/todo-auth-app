from waitress import serve
from main.app.create_flask_app import create_app

if __name__ == "__main__":
    flask_app = create_app(__name__)
    serve(flask_app, host="0.0.0.0", port=8887)
