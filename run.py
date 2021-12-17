from main.app.create_flask_app import create_app

if __name__ == "__main__":
    flask_app = create_app(__name__)
    flask_app.run(debug=True, host='0.0.0.0', port=8887)
# todo - версионирование приложения