from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

from assistant import get_reply as luna_response
from database import init_db

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Initialize database
init_db()

# ---------------- LOGIN MANAGER ---------------- #

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect("luna.db")
    c = conn.cursor()
    c.execute("SELECT id, username FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    conn.close()

    if user:
        return User(user[0], user[1])
    return None

# ---------------- ROUTES ---------------- #

@app.route("/")
@login_required
def home():
    return render_template("index.html", username=current_user.username)

@app.route("/chat", methods=["POST"])
@login_required
def chat():
    message = request.json["message"]

    # Pass username to assistant so it knows who is speaking
    reply = luna_response(message, current_user.username)

    return jsonify({"reply": reply})

# ---------------- REGISTER ---------------- #

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        conn = sqlite3.connect("luna.db")
        c = conn.cursor()

        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
        except:
            conn.close()
            return "Username already exists"

        conn.close()
        return redirect(url_for("login"))

    return render_template("register.html")

# ---------------- LOGIN ---------------- #

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("luna.db")
        c = conn.cursor()
        c.execute("SELECT id, username, password FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            login_user(User(user[0], user[1]))
            return redirect(url_for("home"))

        return "Invalid credentials"

    return render_template("login.html")

# ---------------- LOGOUT ---------------- #

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# ---------------- RUN ---------------- #

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
   



