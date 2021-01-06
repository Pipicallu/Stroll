import os
from flask import (
    Flask, json, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_googlemaps  import GoogleMaps
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
    walks = list(mongo.db.walks.find())
    comments = list(mongo.db.comments.find())
    locations = list(mongo.db.walks.distinct("location"))
    environments = list(mongo.db.walks.distinct("environment"))
    start_point = json.dumps(mongo.db.walks.find_one("start_point"))
    end_point = mongo.db.walks.find_one("end_point")
    # this passes the walks variable so that it may be used in the template
    return render_template("walks.html", walks=walks,
                           start_point=start_point, end_point=end_point,
                           locations=locations, environments=environments,
                           comments=comments)


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    walks = list(mongo.db.walks.find({"$text": {"$search": query}}))
    locations = list(mongo.db.walks.distinct("location"))
    environments = list(mongo.db.walks.distinct("environment"))
    comments = list(mongo.db.comments.find())
    start_point = mongo.db.walks.find_one("start_point")
    end_point = mongo.db.walks.find_one("end_point")
    #This will allow the user to hit enter when blank and be redirected
    if query == "":
        return redirect(url_for("show_walks"))

    return render_template("walks.html", walks=walks,
                           start_point=start_point, end_point=end_point,
                           locations=locations, environments=environments,
                           comments=comments)



@app.route("/comment", methods=["GET", "POST"])
def comment():
    if request.method == "POST":
        new_comment = {
            "comment_index": request.form.get("comment_index"),
            "comment_body": request.form.get("add_comment"),
            "created_by":  session["user"]
        }
        mongo.db.comments.insert_one(new_comment)
        return redirect(url_for("show_walks"))
    walks = list(mongo.db.walks.find())
    start_point = mongo.db.walks.find_one("start_point")
    end_point = mongo.db.walks.find_one("end_point")
    return render_template("walks.html", walks=walks,
                           start_point=start_point, end_point=end_point)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        #looks in the users collection to check if username already exists.
        bio = "Update your Bio and tell the community a little about yourself!"
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
            "posts": startingNumber,
            "bio": bio,
            "img_id": ""
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
    i = 0
    userPosts = list(mongo.db.walks.find({"created_by": session["user"]}))
    postsUpdated = str(len(userPosts))
    usernumber = mongo.db.users.find_one(
        {"username": session["user"]})["_id"]
    profilePic = mongo.db.users.find_one(
        {"username": session["user"]})["img_id"]
    fullName = mongo.db.users.find_one(
        {"username": session["user"]})["full_name"]
    cycles = mongo.db.users.find_one(
        {"username": session["user"]})["cycles"]
    strolls = mongo.db.users.find_one(
        {"username": session["user"]})["strolls"]
    posts = mongo.db.users.find_one(
        {"username": session["user"]})["posts"]
    bio = mongo.db.users.find_one(
        {"username": session["user"]})["bio"]
    for postNo in userPosts:
        i += 1
        if i != len(userPosts):
            mongo.db.users.update_one(
             {"username": session["user"]},
             {"$set": {'posts': postsUpdated}})
    if session["user"]:
        return render_template("profile.html", UserID=fullName,
                               cycles=cycles, strolls=strolls,
                               posts=posts, bio=bio, usernumber=usernumber,
                               profilePic=profilePic)
    else:
        return redirect(url_for('login'))


@app.route("/logout")
def logout():
    # log user out of session
    flash('You have been successfully logged out.')
    session.pop('user')
    return redirect(url_for('login'))


@app.route("/new_walk", methods=["GET", "POST"])
def new_walk():
    if request.method == "POST":
        bikePath = "Y" if request.form.get("bikePath") == "Y" else "N"
        walk = {
            "img_id": request.form.get("image_id"),
            "start_point": {"lat": request.form.get("start-lat"),
                            "lng": request.form.get("start-lng")},
            "end_point":  {"lat": request.form.get("end-lat"),
                           "lng": request.form.get("end-lng")},
            "walk_name": request.form.get("walk_name"),
            "walk_description": request.form.get("walk_description"),
            "environment": request.form.get("environment"),
            "location": request.form.get("location"),
            "distance": request.form.get("distance"),
            "duration": request.form.get("duration"),
            "cycle_duration": request.form.get("cycle_duration"),
            "bike_path": bikePath,
            "difficulty": request.form.get("difficulty"),
            "created_by": session["user"]

        }

        mongo.db.walks.insert_one(walk)
        flash("You Posted a New Walk")
        return redirect(url_for('show_walks'))
    environments = mongo.db.environments.find().sort("environment", 1)
    difficulties = mongo.db.difficulties.find().sort("difficulty", 1)
    return render_template("new_walk.html",
                           environments=environments,
                           difficulties=difficulties)


@app.route("/my_walks")
def my_walks():
    walks = mongo.db.walks.find({"created_by": session["user"]})
    return render_template("my_walks.html", walks=walks)


@app.route("/edit_walk/<walk_id>", methods=["GET", "POST"])
def edit_walk(walk_id):
    if request.method == "POST":
        bikePath = "Y" if request.form.get("bikePath") == "Y" else "N"
        submit = {
            "img_id": request.form.get("image_id"),
            "start_point": {"lat": request.form.get("start-lat"),
                            "lng": request.form.get("start-lng")},
            "end_point":  {"lat": request.form.get("end-lat"),
                           "lng": request.form.get("end-lng")},
            "walk_name": request.form.get("walk_name"),
            "walk_description": request.form.get("walk_description"),
            "environment": request.form.get("environment"),
            "location": request.form.get("location"),
            "distance": request.form.get("distance"),
            "duration": request.form.get("duration"),
            "cycle_duration": request.form.get("cycle_duration"),
            "bike_path": bikePath,
            "difficulty": request.form.get("difficulty"),
            "created_by": session["user"]

        }

        mongo.db.walks.update({"_id": ObjectId(walk_id)}, submit)
        flash("You have Updated your walk")
        return redirect(url_for('my_walks'))
    walk = mongo.db.walks.find_one({"_id": ObjectId(walk_id)})
    environments = mongo.db.environments.find().sort("environment", 1)
    difficulties = mongo.db.difficulties.find().sort("difficulty", 1)
    return render_template("edit_walk.html", walk=walk,
                           environments=environments,
                           difficulties=difficulties)


@app.route("/edit_profile/<User_Id>", methods=["GET", "POST"])
def edit_profile(User_Id):
    # this to pre-render how many posts
    fullName = mongo.db.users.find_one(
        {"username": session["user"]})["full_name"]
    email = mongo.db.users.find_one(
        {"_id": ObjectId(User_Id)})['email_address']
    password = mongo.db.users.find_one(
        {"_id": ObjectId(User_Id)})['password']
    username = mongo.db.users.find_one(
        {"_id": ObjectId(User_Id)})['username']
    if request.method == "POST":
        userUpdated = {
          "img_id": request.form.get("image_id"),
          "email_address": email,
          "full_name": request.form.get('fullName'),
          "username": username,
          "password": password,
          "strolls": request.form.get('strolls'),
          "cycles": request.form.get('cycles'),
          "posts": request.form.get('posts'),
          "bio": request.form.get('bio')
        }
        mongo.db.users.update({"_id": ObjectId(User_Id)}, userUpdated)
        flash('Profile Updated')
        return redirect(url_for('profile',  UserID=fullName))
    user = mongo.db.users.find_one({"_id": ObjectId(User_Id)})
    return render_template('edit_profile.html', user=user)


@app.route("/delete_walk/<walk_id>")
def delete_walk(walk_id):
    walks = mongo.db.walks.find({"created_by": session["user"]})
    mongo.db.walks.remove({"_id": ObjectId(walk_id)})
    flash("You have deleted this stroll!")
    return redirect(url_for('my_walks', walks=walks))


# If the module (python file being run) is the main
# one then this is from where to run our application
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)