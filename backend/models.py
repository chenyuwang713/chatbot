from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize database
db = SQLAlchemy()

# User model
class User(db.Model):
    __tablename__ = "user"  # Ensure a valid table name (not "user")
     
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    identifier = db.Column(db.String(32), unique=True, nullable=False)
    consent_given = db.Column(db.Boolean, default=False)  # ✅ Track consent

# Response model
class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
class Chat(db.Model):
    __tablename__ = "chat"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Add primary key
    identifier = db.Column(db.String(255), nullable=False)
    sender = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    

class Survey(db.Model):
    __tablename__ = "surveys"  # Ensure a unique table name

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(32), unique=True, nullable=False)  # Unique user ID
    race = db.Column(db.String(100), nullable=False)
    race_other = db.Column(db.String(100), nullable=True)
    gender = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    role_other = db.Column(db.String(100), nullable=True)
    experience = db.Column(db.String(50), nullable=False)
    school_type = db.Column(db.String(100), nullable=False)
    school_other = db.Column(db.String(100), nullable=True)
    ai_usage = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)   
    

# Admin model
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

# Function to initialize database
def init_db():
    """Create tables if they don't exist."""
    with db.engine.connect() as connection:
        db.create_all()