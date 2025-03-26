from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from models import db
from routes import routes
from config import Config
from database import create_default_admin  # Import AFTER initializing db

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)  # Ensure this is only called once
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Register routes
app.register_blueprint(routes)


CORS(app, resources={r"/*": {"origins": "http://18.119.102.36:8080"}}, supports_credentials=True)

# Ensure an admin is created at startup
with app.app_context():
    db.create_all()  
    create_default_admin() 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)