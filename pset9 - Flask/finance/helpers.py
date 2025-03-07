import requests
import re
from flask import redirect, render_template, session
from functools import wraps

def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def lookup(symbol):
    """Look up quote for symbol."""
    url = f"https://finance.cs50.io/quote?symbol={symbol.upper()}"
    try:
        response = requests.get(url)
        response.raise_for_status() 
        quote_data = response.json()
        return {
            "price": quote_data["latestPrice"],
            "symbol": symbol.upper()
        }
    
    except requests.RequestException as e:
        print(f"Request error: {e}")
    except (KeyError, ValueError) as e:
        print(f"Data parsing error: {e}")
    print("Resultado da API:", response.json())  # Para ver a resposta da API
    return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"

def validate_password(password):
    """Verifica se a senha atende aos requisitos mínimos"""
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not re.search(r"\d", password):  # Verifica se tem pelo menos um número
        return "Password must contain at least one number."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):  # Verifica se tem pelo menos um símbolo especial
        return "Password must contain at least one special character (!@#$%^&*(),.?\":{}|<>)."
    return None  # Senha válida
