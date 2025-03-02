import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
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
    stocks = db.execute("SELECT symbol, SUM(shares) AS shares FROM portfolio WHERE user_id = ? GROUP BY symbol", session["user_id"])

    total_value = 0
    for stock in stocks:
        stock_info = lookup(stock["symbol"])
        if stock_info:
            stock["price"] = stock_info["price"]
            stock["total"] = stock["shares"] * stock["price"]
            total_value += stock["total"]

    user = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    cash = user[0]["cash"]

    return render_template("index.html", stocks=stocks, cash=cash, total=total_value + cash)

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
    transactions = db.execute(
        "SELECT symbol, shares, price FROM transactions WHERE user_id = ? ORDER BY id DESC",
        session["user_id"]
    )

    return render_template("history.html", transactions=transactions)

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
        if not stock:
            return apology("Invalid symbol", 400)
        return render_template("quote.html", stock=stock)
    return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password or not confirmation:
            return apology("Fill in all fields", 400)

        if password != confirmation:
            return apology("Passwords do not match", 400)

        hash_password = generate_password_hash(password)

        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash_password)
        except:
            return apology("User already exists", 400)

        return redirect("/login")

    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
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
            return apology("Not enough shares", 400)

        stock = lookup(symbol)
        if not stock:
            return apology("Invalid symbol", 400)

        price = stock["price"]
        revenue = shares * price

        db.execute("UPDATE portfolio SET shares = shares - ? WHERE user_id = ? AND symbol = ?", shares, session["user_id"], symbol)
        db.execute("DELETE FROM portfolio WHERE shares = 0")

        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", revenue, session["user_id"])

        db.execute("""
            INSERT INTO transactions (user_id, symbol, shares, price)
            VALUES (?, ?, ?, ?) """, session["user_id"], symbol, shares, price)
        
        flash("Stock sold successfully!")
        return redirect("/")
    
    return render_template("sell.html")
