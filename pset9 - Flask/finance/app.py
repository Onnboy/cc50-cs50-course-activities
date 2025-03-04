import os
import sqlite3
from cs50 import SQL
from flask import Flask, render_template, url_for, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup, usd

app = Flask(__name__)

app.jinja_env.filters["usd"] = usd

DATABASE_PATH = os.path.join(os.getcwd(), "finance.db")

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row 
    return conn

conn = get_db_connection()
db = conn.cursor()
db.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = db.fetchall()
conn.close()

app.jinja_env.filters["usd"] = usd

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///finance.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session.get("user_id")
    if not user_id:
        flash("User not logged in.", "danger")
        return redirect(url_for("login"))
    
    try:
        user = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        cash = user[0]["cash"] if user else 0
        total = cash 
    except Exception as e:
        flash(f"Error fetching user data: {str(e)}", "danger")
        return redirect(url_for("index"))

    return render_template("index.html", cash=cash, total=total)

@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    if "user_id" not in session:
        flash("You must be logged in to change your password.", "warning")
        return redirect("/login")

    if request.method == "POST":
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        if not current_password or not new_password or not confirm_password:
            flash("All fields are required.", "danger")
            return redirect("/change_password")

        if new_password != confirm_password:
            flash("New passwords do not match.", "danger")
            return redirect("/change_password")

        conn = sqlite3.connect("finance.db")
        db = conn.cursor()
    
        db.execute("SELECT hash FROM users WHERE id = ?", (session["user_id"],))
        row = db.fetchone()
        
        print("Tabelas existentes:", db.fetchall())  # Isso mostrará todas as tabelas disponíveis no terminal

        if not row or not check_password_hash(row[0], current_password):
            flash("Current password is incorrect.", "danger")
            conn.close()
            return redirect("/change_password")

        hashed_password = generate_password_hash(new_password)
        db.execute("UPDATE users SET hash = ? WHERE id = ?", (hashed_password, session["user_id"]))
        conn.commit()
        conn.close()

        flash("Password successfully changed!", "success")
        return redirect("/")

    return render_template("change_password.html")



@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        try:
            shares = int(request.form.get("shares"))
            if shares <= 0:
                return apology("Invalid number of shares", 400)
        except ValueError:
            return apology("Shares must be a positive integer", 400)

        stock = lookup(symbol)
        if not stock:
            return apology("Invalid symbol", 400)

        price = stock["price"]
        cost = shares * price

        user = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash = user[0]["cash"]

        if cost > cash:
            return apology("Not enough funds", 400)

        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", cost, session["user_id"])

        db.execute("""
            INSERT INTO portfolio (user_id, symbol, shares)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id, symbol) 
            DO UPDATE SET shares = portfolio.shares + excluded.shares
            """, session["user_id"], symbol, shares)
        db.execute("""
            INSERT INTO transactions (user_id, symbol, shares, price)
            VALUES (?, ?, ?, ?) """, session["user_id"], symbol, shares, price)
        
        flash("Stock purchased successfully!")
        return redirect("/")
    
    return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session.get("user_id")
    if not user_id:
        flash("User not logged in.", "danger")
        return redirect(url_for("login"))
    
    try:
        transactions = db.execute("SELECT symbol, shares, price, transacted FROM transactions WHERE user_id = ? ORDER BY transacted DESC", user_id)
        cash_transactions = db.execute("SELECT amount, status, timestamp FROM cash_transactions WHERE user_id = ?", user_id)
    except Exception as e:
        flash(f"Error fetching history: {str(e)}", "danger")
        return redirect(url_for("index"))

    return render_template("history.html", transactions=transactions, cash_transactions=cash_transactions)

@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    """User can add cash"""
    if request.method == "GET":
        return render_template("add_cash.html")
    
    else:
        try:
            new_cash = float(request.form.get("new_cash"))
            if new_cash <= 0:
                flash("Amount must be a positive number.", "danger")
                return redirect(url_for("add_cash"))
        except ValueError:
            flash("Invalid amount entered.", "danger")
            return redirect(url_for("add_cash"))

        user_id = session.get("user_id")
        if not user_id:
            flash("User not logged in.", "danger")
            return redirect(url_for("login"))

        try:
            db.execute("INSERT INTO cash_transactions (user_id, amount, status) VALUES (?, ?, 'Approved')",
                       user_id, new_cash)
            
            db.execute("UPDATE users SET cash = cash + ? WHERE id = ?",
                       new_cash, user_id)
            
            flash(f"Successfully added ${new_cash:.2f}!", "success")
            return redirect(url_for("history"))
        
        except Exception as e:
            flash(f"Database error: {str(e)}", "danger")
            return redirect(url_for("add_cash"))
 

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()

    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must provide username", 403)
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        stock = lookup(symbol)
        
        name = stock.get("name", stock["symbol"])

        if not stock or "price" not in stock or "symbol" not in stock:
            return apology("Invalid symbol or API error", 400)

        return render_template("quoted.html", name=name, price=usd(stock["price"]), symbol=stock["symbol"])

    return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password or not confirmation:
            return apology("Fill in all fields", 400)

        if password != confirmation:
            return apology("Passwords do not match", 400)

        hash_password = generate_password_hash(password)

        try:
            new_user = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash_password)
        except:
            return apology("User already exists", 400)

        session["user_id"] = new_user
        return redirect("/login")

    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    stocks = db.execute("SELECT symbol FROM portfolio WHERE user_id = ?", session["user_id"])
    symbols = [stock["symbol"] for stock in stocks]

    if request.method == "POST":
        symbol = request.form.get("symbol")
        try:
            shares = int(request.form.get("shares"))
            if shares <= 0:
                return apology("Invalid number of shares", 400)
        except ValueError:
            return apology("Shares must be a positive integer", 400)

        stock_owned = db.execute(
            "SELECT shares FROM portfolio WHERE user_id = ? AND symbol = ?", session["user_id"], symbol
        )
        if not stock_owned or stock_owned[0]["shares"] < shares:
            return apology("Insufficient actions", 400)

        stock = lookup(symbol)
        if not stock:
            return apology("Invalid symbol", 400)

        price = stock["price"]
        revenue = shares * price

        db.execute("UPDATE portfolio SET shares = shares - ? WHERE user_id = ? AND symbol = ?", shares, session["user_id"], symbol)
        db.execute("DELETE FROM portfolio WHERE user_id = ? AND symbol = ? AND shares = 0", session["user_id"], symbol)

        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", revenue, session["user_id"])

        db.execute("""
            INSERT INTO transactions (user_id, symbol, shares, price)
            VALUES (?, ?, ?, ?) """, session["user_id"], symbol, -shares, price)

        flash("Sold successfully!")
        return redirect("/")

    return render_template("sell.html", symbols=symbols)

