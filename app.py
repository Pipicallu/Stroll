import os
from flask import (
    Flask, flash, render_template, 
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId

if os.path.exists("env.py"):
    import env


app = Flask(__name__)

# grab the database name
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/show_walks")
def show_walks():
    walks = mongo.db.walks.find()
    #this passes the walks variable so that it may be used in the template 
    return render_template("walks.html", walks=walks)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        #looks in the users collection to check if username already exists.
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("UserID").lower()})
        existing_email = mongo.db.users.find_one(
            {"email_address": request.form.get("Email").lower()})
        if existing_user:
            flash("Username already exists")
            return redirect(url_for('register'))
        elif existing_email:
            flash("A user with this email address already exists.")
            return redirect(url_for("register"))
        register = {
            "email_address": request.form.get("Email").lower(),
            "full_name": request.form.get("FullName"),
            "username": request.form.get("UserID").lower(),
            "password": generate_password_hash(request.form.get('password'))
        }
        mongo.db.users.insert_one(register)
        # put the user information into a session cookie so that they are remembered by the website.
        session["user"] = request.form.get('UserID').lower()
        flash("Registration Successful!")
    return render_template("register.html")


# If the module (python file being run) is the main
# one then this is from where to run our application
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)