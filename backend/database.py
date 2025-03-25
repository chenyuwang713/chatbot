from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from models import Admin
import os

db = SQLAlchemy()
bcrypt = Bcrypt()

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        create_default_admin()

from models import db, Admin
from flask_bcrypt import Bcrypt
import os

bcrypt = Bcrypt()

def create_default_admin():
    """Ensure an admin account exists at startup."""
    from app import app  # Import app to ensure it's initialized

    with app.app_context():
        admin_email = os.getenv("ADMIN_EMAIL")
        admin_password = os.getenv("ADMIN_PASSWORD")

        # Check if the admin user exists
        existing_admin = Admin.query.filter_by(email=admin_email).first()
        if not existing_admin:
            hashed_password = bcrypt.generate_password_hash(admin_password).decode('utf-8')
            new_admin = Admin(email=admin_email, password_hash=hashed_password)
            db.session.add(new_admin)
            db.session.commit()
            print(f"Admin created: {admin_email}")