import os
from flask import (
    Flask, json, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_googlemaps import GoogleMaps
import cloudinary as Cloud
from bson.objectid import ObjectId


if os.path.exists("env.py"):
    import env


app = Flask(__name__)

# grab the database name
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

app.config['GOOGLEMAPS_KEY'] = os.environ.get("GOOGLEMAPS_KEY")

Cloud.config.update = ({
    'cloud_name': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'api_key': os.environ.get('CLOUDINARY_API_KEY'),
    'api_secret': os.environ.get('CLOUDINARY_API_SECRET')
})




GoogleMaps(app)
mongo = PyMongo(app)


@app.route("/")
@app.route("/show_walks")
def show_walks():
    hydePark = Cloud.CloudinaryImage("HydePark.jpg")
    walks = list(mongo.db.walks.find())
    start_point = json.dumps(mongo.db.walks.find_one("start_point"))
    end_point = mongo.db.walks.find_one("end_point")
    #this passes the walks variable so that it may be used in the template 
    return render_template("walks.html", walks=walks,
                           start_point=start_point, end_point=end_point,
                           hydePark=hydePark)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        #looks in the users collection to check if username already exists.
        startingNumber = int("0")
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
            "password": generate_password_hash(request.form.get('password')),
            "strolls": startingNumber,
            "cycles": startingNumber,
            "posts": startingNumber
        }
        mongo.db.users.insert_one(register)
        # put the user information into a session cookie so that they are remembered by the website.
        session["user"] = request.form.get('UserID').lower()
        flash("Registration Successful!")
        return redirect(url_for('profile', UserID=session["user"]))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
    # here we are checking to see if there is already an existing user in the db
        existing_user = mongo.db.users.find_one(
                {"username": request.form.get("UserID").lower()})
        if existing_user:
    # here we are checking to see that the password matches against the one placed in the form
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get('UserID').lower()
                flash("Welcome {}".format(request.form.get('UserID')))
                return redirect(url_for('profile', UserID=session["user"]))
            else:
                flash("Incorrect Username and/or Password, Please try again.")
                return redirect(url_for("login"))
        else:
            flash("Incorrect Username and/or Password, Please try again.")
            return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/profile/<UserID>", methods=["GET", "POST"])
def profile(UserID):
    fullName = mongo.db.users.find_one(
        {"username": session["user"]})["full_name"]
    cycles = mongo.db.users.find_one(
        {"username": session["user"]})["cycles"]
    strolls = mongo.db.users.find_one(
        {"username": session["user"]})["strolls"]
    posts = mongo.db.users.find_one(
        {"username": session["user"]})["posts"]
    if session["user"]:
        return render_template("profile.html", UserID=fullName,
                               cycles=cycles, strolls=strolls, posts=posts)
    else:
        return redirect(url_for('login'))

@app.route("/logout")
def logout():
    #log user out of session 
    flash('You have been successfully logged out.')
    session.pop('user')
    return redirect(url_for('login'))


@app.route("/new_walk")
def new_walk():
    return render_template("new_walk.html")

# If the module (python file being run) is the main
# one then this is from where to run our application
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)