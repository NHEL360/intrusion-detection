from flask import Flask, render_template, request, redirect, url_for, session, flash
import time
from werkzeug.security import generate_password_hash, check_password_hash  # For secure password storage

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Simulating a simple "database" for users and roles
users_db = {
    "admin": {"password": generate_password_hash("admin123"), "role": "admin", "failed_attempts": 0, "last_failed_time": 0},
    "user1": {"password": generate_password_hash("user123"), "role": "user", "failed_attempts": 0, "last_failed_time": 0},
    "user2": {"password": generate_password_hash("password123"), "role": "user", "failed_attempts": 0, "last_failed_time": 0}
}

# Maximum allowed failed login attempts and lockout time
MAX_FAILED_ATTEMPTS = 3
LOCKOUT_TIME = 60  # Time in seconds for lockout (1 minute)

# Home route (root URL)
@app.route("/")
def home():
    return render_template("home.html")  # Render an HTML template for the home page

# Login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        
        # Check if the user exists
        if username in users_db:
            user = users_db[username]
            current_time = time.time()

            # Check if account is locked due to too many failed attempts
            if user["failed_attempts"] >= MAX_FAILED_ATTEMPTS and current_time - user["last_failed_time"] < LOCKOUT_TIME:
                flash("Account is locked due to too many failed attempts. Please try again later.")
                return redirect(url_for('login'))

            # Validate credentials using password hash
            if check_password_hash(user["password"], password):
                session['user'] = username
                session['role'] = user['role']
                user["failed_attempts"] = 0  # Reset failed attempts on successful login
                flash("Login successful!")
                return redirect(url_for('dashboard'))
            else:
                # Increment failed attempts and set lockout time
                user["failed_attempts"] += 1
                user["last_failed_time"] = current_time
                flash("Invalid credentials. Please try again.")
                return redirect(url_for('login'))
        else:
            flash("User not found.")
            return redirect(url_for('login'))
    
    return render_template('login.html')

# Additional routes and logic for dashboards...

if __name__ == "__main__":
    app.run(debug=True, port=5001)
