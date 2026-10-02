from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import pickle
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "email-spam-detector-secret-key"
with open("spam_model.pkl", "rb") as file:
    model = pickle.load(file)

def get_db_connection():
    connection = sqlite3.connect("users.db")
    connection.row_factory = sqlite3.Row
    return connection


@app.route("/")
def login():
    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            return "Passwords do not match. Please go back and try again."

        connection = get_db_connection()

        existing_user = connection.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        if existing_user:
            connection.close()
            return "This email is already registered. Please login."

        hashed_password = generate_password_hash(password)

        connection.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (email, hashed_password)
        )

        connection.commit()
        connection.close()

        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login_user():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        connection = get_db_connection()

        user = connection.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        connection.close()

        if user and check_password_hash(user["password"], password):

            session["user_email"] = email

            return redirect(url_for("home"))

        return "Invalid email or password. Please try again."

    return render_template("login.html")


@app.route("/home")
def home():

    if "user_email" not in session:
        return redirect(url_for("login"))

    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    if "user_email" not in session:
        return redirect(url_for("login"))

    email_text = request.form["email_text"]

    prediction = model.predict([email_text])[0]

    if prediction == "spam":
        result = "🚨 Spam Email"
    else:
        result = "✅ Not Spam"

    return render_template(
        "index.html",
        result=result,
        email_text=email_text
    )


if __name__ == "__main__":
    app.run(debug=True)