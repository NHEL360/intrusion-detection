from flask import Flask, render_template, request, redirect, url_for, session, flash
import time

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SESSION_PERMANENT'] = False  # Ensures session is cleared after closing browser

# Simulated user database
users_db = {
    "admin": {"password": "admin123", "role": "admin", "failed_attempts": 0, "last_failed_time": 0},
    "user1": {"password": "user123", "role": "user", "failed_attempts": 0, "last_failed_time": 0},
    "user2": {"password": "password123", "role": "user", "failed_attempts": 0, "last_failed_time": 0}
}

MAX_FAILED_ATTEMPTS = 3
LOCKOUT_TIME = 60  # 1 minute lockout

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        if username in users_db:
            user = users_db[username]
            current_time = time.time()

            # Lockout check
            if user["failed_attempts"] >= MAX_FAILED_ATTEMPTS and (current_time - user["last_failed_time"] < LOCKOUT_TIME):
                flash("Account locked. Try again later.", "error")
                return redirect(url_for('login'))

            if user["password"] == password:
                session['user'] = username
                session['role'] = user['role']
                user["failed_attempts"] = 0  # Reset failed attempts
                flash("Login successful!", "success")
                return redirect(url_for('dashboard'))
            else:
                user["failed_attempts"] += 1
                user["last_failed_time"] = current_time
                flash("Invalid credentials. Try again.", "error")
        else:
            flash("User not found.", "error")

    return render_template('login.html')

@app.route("/dashboard")
def dashboard():
    if 'user' in session:
        return redirect(url_for('admin_dashboard' if session['role'] == 'admin' else 'user_dashboard'))
    flash("Please log in first.", "warning")
    return redirect(url_for('login'))

@app.route("/admin")
def admin_dashboard():
    if 'user' in session and session['role'] == 'admin':
        return render_template('admin_dashboard.html')
    flash("Unauthorized access.", "error")
    return redirect(url_for('login'))

@app.route("/user")
def user_dashboard():
    if 'user' in session and session['role'] == 'user':
        return render_template('user_dashboard.html')
    flash("Unauthorized access.", "error")
    return redirect(url_for('login'))

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True, port=5001)
