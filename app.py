from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from helpers import apology, login_required
from werkzeug.security import check_password_hash, generate_password_hash
import re
import sqlite3

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def get_db_connection():
    conn = sqlite3.connect("bmicalculator.db")
    return conn, conn.cursor()

def create_users_table():
    conn = sqlite3.connect("bmicalculator.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            hash TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

@app.route('/')
@login_required
def hello_world():
    # Get the user ID from the session
    user_id = session.get("user_id")

    if user_id is not None:
        # Query the database to get the username for the current user
        conn, cursor = get_db_connection()
        cursor.execute("SELECT username FROM users WHERE id = ?", (user_id,))
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            # user_data[0] contains the username
            username = user_data[0]
        else:
            # Handle the case where user_id is not found in the database
            username = "Unknown User"  

    return render_template("index.html", username=username)



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query db for username
        conn, cursor = get_db_connection()
        cursor.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
        rows = cursor.fetchall()
        conn.close()

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0][2], request.form.get("password")
        ):
            return apology("Invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0][0]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Validate data
        if not username:
            return apology("Username cannot be blank.")

        if not password:
            return apology("Password cannot be blank.")

        if password != confirmation:
            return apology("Passwords do not match.")

        # Check if password meets the complexity requirements

        if not re.match(
            r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$", password
        ):
            return apology(
                "Password must have at least 8 characters, including letters, numbers and special symbols."
            )

         # Check if username already exists
        conn, cursor = get_db_connection()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        rows = cursor.fetchall()

        if rows:
            conn.close()
            return apology("Username already exists.")

        # Hash the password before storing it
        hashed_password = generate_password_hash(password)

        # Insert data into db
        cursor.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        conn.close()

        # Redirect user to login page
        return redirect("/login")

    # If request.method == "GET":
    return render_template("register.html")

if __name__ == "__main__":
    create_users_table()  # Create the "users" table if it doesn't exist
    app.run()
