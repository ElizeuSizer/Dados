import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User
from forms import RegisterForm, LoginForm
import bcrypt

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "devsecret")

# --- FIX DA URL DO BANCO (psycopg3) ---
uri = os.getenv("DATABASE_URL", "").strip()
if not uri:
    raise RuntimeError("DATABASE_URL não definido nas variáveis de ambiente.")

# Render/Neon costumam fornecer "postgresql://..." (ou às vezes "postgres://")
# Precisamos converter para o dialeto do psycopg3:
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql+psycopg://", 1)
elif uri.startswith("postgresql://"):
    uri = uri.replace("postgresql://", "postgresql+psycopg://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = uri
# --------------------------------------

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True,
    "pool_recycle": 1800,
}

if os.getenv("RENDER"):
    app.config.update(
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
    )

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

with app.app_context():
    db.create_all()

