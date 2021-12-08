db = db.getSiblingDB('todo_app_db');

db.createCollection('user_token');

db.createUser(
{
	user: "todo_app_admin",
	pwd: "todo_app_admin",
	roles:[
	    {role: "readWrite" , db:"todo_app_db"}
	]}
)
