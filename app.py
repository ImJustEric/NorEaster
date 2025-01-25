import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, g
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required


# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///skiing.db")

# Check if user is logged into display username as hello
@app.before_request
def load_user():
    if "user_id" in session:
        g.username = db.execute("SELECT username FROM users WHERE id = :id", id=session["user_id"])

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if not request.form.get("username"):
            error_message = "Input valid username"
            return render_template("register.html", error_message=error_message)
        # Ensure password was submitted
        elif not request.form.get("password"):
            error_message = "Input valid password"
            return render_template("register.html", error_message=error_message)
        # Ensure a confirmation was submitted
        elif not request.form.get("confirmation"):
            error_message = "Input valid password confirmation"
            return render_template("register.html", error_message=error_message)
        # Ensure password matches confirmation
        elif request.form.get("password") != request.form.get("confirmation"):
            error_message = "Passwords do not match"
            return render_template("register.html", error_message=error_message)
        check = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(check) != 0:
            error_message = "Username already exists"
            return render_template("register.html", error_message=error_message)
        # Hash password and insert into database
        hash = generate_password_hash(request.form.get("password"))
        row = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=request.form.get("username"), hash=hash)
        # Automatically log user back in
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        session["user_id"] = rows[0]["id"]
        # Return back to homepage
        return redirect("/")
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            error_message = "Invalid Username "
            return render_template("login.html", error_message=error_message)
        # Ensure password was submitted
        elif not request.form.get("password"):
            error_message = "Invalid Password "
            return render_template("login.html", error_message=error_message)
        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username"))
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            error_message = "Username or password do not match"
            return render_template("login.html", error_message=error_message)
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        # Redirect user to home page
        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/map")
def map():
    return render_template("map.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    resorts = db.execute("SELECT name, resorts.min_elevation, region, resorts.max_elevation, resort_id, SUM(CASE WHEN difficulty = 'easy' THEN count ELSE 0 END) AS easy_count, SUM(CASE WHEN difficulty = 'intermediate' THEN count ELSE 0 END) AS medium_count, SUM(CASE WHEN difficulty = 'advanced' THEN count ELSE 0 END) AS hard_count, SUM(CASE WHEN difficulty = 'other' THEN count ELSE 0 END) AS other_count FROM resorts JOIN runs ON resorts.id=resort_id GROUP BY name")
    if request.method == "POST":
        # Check for index search query
        resort_search = request.form.get("resort-search") or request.form.get("search-page-search")
        if resort_search:
            resorts = db.execute("SELECT name, resorts.min_elevation, region, resorts.max_elevation, resort_id, SUM(CASE WHEN difficulty = 'easy' THEN count ELSE 0 END) AS easy_count, SUM(CASE WHEN difficulty = 'intermediate' THEN count ELSE 0 END) AS medium_count, SUM(CASE WHEN difficulty = 'advanced' THEN count ELSE 0 END) AS hard_count, SUM(CASE WHEN difficulty = 'other' THEN count ELSE 0 END) AS other_count FROM resorts JOIN runs ON resorts.id=resort_id WHERE name LIKE :resort_search GROUP BY name", resort_search=resort_search+'%')
            return render_template("search.html", resorts=resorts)
        # Grab values of the checkbox
        checklist = request.form.getlist('region')

        # Grab all filter requests and assign a default value if a filter is left blank
        minimum_min = int(request.form.get('minimum-min')) if request.form.get('minimum-min') else 0
        minimum_max = int(request.form.get('minimum-max')) if request.form.get('minimum-max') else 1000000
        maximum_min = int(request.form.get('maximum-min')) if request.form.get('maximum-min') else 0
        maximum_max = int(request.form.get('maximum-max')) if request.form.get('maximum-max') else 100000
        easy_min = int(request.form.get('easy-min')) if request.form.get('easy-min') else 0
        easy_max = int(request.form.get('easy-max')) if request.form.get('easy-max') else 100
        med_min = int(request.form.get('med-min')) if request.form.get('med-min') else 0
        med_max = int(request.form.get('med-max')) if request.form.get('med-max') else 100
        adv_min = int(request.form.get('adv-min')) if request.form.get('adv-min') else 0
        adv_max = int(request.form.get('adv-max')) if request.form.get('adv-max') else 100

        placeholders = ', '.join(['?'] * len(checklist))
        query = f"SELECT name, resorts.min_elevation, region, resorts.max_elevation, resort_id, SUM(CASE WHEN difficulty = 'easy' THEN count ELSE 0 END) AS easy_count, SUM(CASE WHEN difficulty = 'intermediate' THEN count ELSE 0 END) AS medium_count, SUM(CASE WHEN difficulty = 'advanced' THEN count ELSE 0 END) AS hard_count, SUM(CASE WHEN difficulty = 'other' THEN count ELSE 0 END) AS other_count FROM resorts JOIN runs ON resorts.id=resort_id WHERE region IN ({placeholders}) GROUP BY name"
        # If nothing is checked then display everything using other filters
        if len(checklist) == 0:
            resorts = resorts = db.execute("SELECT name, resorts.min_elevation, region, resorts.max_elevation, resort_id, SUM(CASE WHEN difficulty = 'easy' THEN count ELSE 0 END) AS easy_count, SUM(CASE WHEN difficulty = 'intermediate' THEN count ELSE 0 END) AS medium_count, SUM(CASE WHEN difficulty = 'advanced' THEN count ELSE 0 END) AS hard_count, SUM(CASE WHEN difficulty = 'other' THEN count ELSE 0 END) AS other_count FROM resorts JOIN runs ON resorts.id=resort_id WHERE resorts.min_elevation > :minimum_min AND resorts.min_elevation < :minimum_max AND resorts.max_elevation > :maximum_min AND resorts.max_elevation < :maximum_max GROUP BY NAME HAVING easy_count > :easy_min AND easy_count < :easy_max AND medium_count > :med_min AND medium_count < :med_max AND hard_count > :adv_min AND hard_count < :adv_max", minimum_min=minimum_min, minimum_max=minimum_max, maximum_min=maximum_min, maximum_max=maximum_max, easy_min=easy_min, easy_max=easy_max, med_min=med_min, med_max=med_max, adv_min=adv_min, adv_max=adv_max)
            return render_template("search.html", resorts=resorts)
        resorts = db.execute(query, *checklist)
        return render_template("search.html", resorts=resorts)
    else:
        return render_template("search.html", resorts=resorts)


@app.route("/add-to-checklist", methods=["POST"])
@login_required
def add_to_checklist():
    resort_id = request.form.get('resort-id')
    resort_name = db.execute("SELECT name FROM resorts WHERE id = :id", id=resort_id)[0]['name']
    # Check if the resort is already in checklist, otherwise insert
    checklist = db.execute("SELECT * FROM checklist WHERE mountain_name = :resort_name AND person_id=:person_id", resort_name = resort_name, person_id=session["user_id"])
    if checklist:
        flash("Resort already exists in checklist.")
        return redirect("/checklist")
    else:
        insert_checklist = db.execute("INSERT INTO checklist (person_id, mountain_id, mountain_name) VALUES (:id, :resort_id, :resort_name)", id=session["user_id"], resort_id=resort_id, resort_name=resort_name)
        flash("Added to checklist!", "success")
        return redirect("/checklist")

@app.route("/checklist", methods=["GET", "POST"])
@login_required
def checklist():
    resorts = db.execute("SELECT * FROM checklist WHERE person_id = :id", id=session["user_id"])
    if request.method == "POST":
        # If remove button pressed then delete item from checklist
        if "checklist-remove" in request.form:
            checklist_id = request.form.get("checklist-id")
            remove_checklist = db.execute("DELETE FROM checklist WHERE id=:checklist_id", checklist_id=checklist_id)
            resorts = db.execute("SELECT * FROM checklist WHERE person_id = :id", id=session["user_id"])
            return render_template("checklist.html", resorts=resorts)
        # If submit button pressed then add comment to database
        if "checklist-submit" in request.form:
            checklist_id = request.form.get("checklist-id")
            resort_comment = request.form.get("comment")
            insert_comment = db.execute("UPDATE checklist SET comment = :resort_comment WHERE id = :checklist_id", resort_comment=resort_comment, checklist_id=checklist_id)
            resorts = db.execute("SELECT * FROM checklist WHERE person_id = :id", id=session["user_id"])
            return render_template("checklist.html", resorts=resorts)
    else:
        return render_template("checklist.html", resorts=resorts)
