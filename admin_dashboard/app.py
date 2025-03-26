from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "postgresql://user:password@db/surveydb")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "supersecretkey")

db = SQLAlchemy(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)




CORS(app, resources={r"/admin/*": {"origins": "http://18.119.102.36:3001"}}, supports_credentials=True, allow_headers=["Content-Type"])
# Admin model
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

@app.route("/admin/register", methods=["POST"])
def register():
    data = request.json
    email = data["email"]
    password = data["password"]
    
    if Admin.query.filter_by(email=email).first():
        return jsonify({"error": "Admin already exists"}), 400
    
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    new_admin = Admin(email=email, password_hash=hashed_password)
    db.session.add(new_admin)
    db.session.commit()
    return jsonify({"message": "Admin registered successfully"}), 201

@app.route("/admin/login", methods=["POST"])
def login():
    data = request.json
    email = data["email"]
    password = data["password"]
    
    admin = Admin.query.filter_by(email=email).first()
    if not admin or not bcrypt.check_password_hash(admin.password_hash, password):
        return jsonify({"error": "Invalid credentials"}), 401
    
    access_token = create_access_token(identity=admin.email)
    return jsonify({'access_token': access_token}), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=3000, debug=True)