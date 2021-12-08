from main.app.create_flask_app import create_app
from pymongo import MongoClient


if __name__ == "__main__":
    # client = MongoClient('mongodb://todo_app_admin:todo_app_admin@localhost:27017/todo_app_db')
    # db = client['todo_app_db']
    # collection = db['user_token']
    # print(collection.find_one())
    # print(db.list_collection_names())
    flask_app = create_app(__name__)
    flask_app.run(debug=True, host='0.0.0.0', port=8887)
