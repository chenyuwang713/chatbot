survey-system/
│── admin_dashboard/               # Admin Dashboard (React or Flask-based)
│   ├── static/                    # Static files (CSS, JS, images)
│   ├── templates/                 # HTML templates
│   ├── app.py                     # Admin dashboard backend (if using Flask)
│   ├── requirements.txt            # Python dependencies (Flask, SQLAlchemy, etc.)
│   ├── package.json                # Dependencies (if using React)
%│   ├── src/                        # React frontend source (if applicable)

        ── src/
        │   ├── components/               # UI Components
        │   │   ├── EmailUploader.js      # Upload emails feature
        │   │   ├── ResponseList.js       # Display user responses
        │   │   ├── Navbar.js             # Navigation bar for the dashboard
        │   │   ├── LogoutButton.js       # Logout functionality
        │   │   ├── ProtectedRoute.js     # Ensures authenticated access
        │   │
        │   ├── pages/                    # Page-level components
        │   │   ├── AdminDashboard.js     # Main dashboard page
        │   │   ├── Login.js              # Admin login page
        │   │
        │   ├── App.js                    # Main React entry component
        │   ├── index.js                  # React DOM root
        │   ├── api.js                    # Axios API configuration
        │   ├── auth.js                    # Auth helper functions
        │

│   ├── Dockerfile                  # Docker setup for Admin Dashboard
│
│── backend/                        # Backend API (Flask)
│   ├── app.py                      # Main Flask application
│   ├── models.py                   # Database models
│   ├── routes.py                   # API endpoints
│   ├── database.py                  # Database connection and initialization
│   ├── config.py                    # Configuration settings
│   ├── requirements.txt             # Python dependencies
│   ├── Dockerfile                   # Docker setup for backend
│
│── db/                              # Database initialization
│   ├── init.sql                     # SQL script to create tables (optional)
│
│── web/                             # Frontend (HTML, CSS, JS for survey pages)
│   ├── index.html                   # Consent page
│   ├── survey.html                  # Survey page
│   ├── noagree.html                 # Decline participation page
│   ├── chatbot.html                  # Chatbot interface after survey
│   ├── static/                       # Static assets (CSS, JS, images)
│   ├── Dockerfile                    # Docker setup for web service
│
│── docker-compose.yml                # Docker Compose for orchestrating services
│── .env                               # Environment variables (API keys, DB credentials)
│── README.md                          # Documentation on setup and usage




user1@example.com
user2@example.com
user3@example.com


 document.querySelectorAll('input[name="race"]').forEach(radio => {
              radio.addEventListener("change", function() {
                  document.getElementById("race_other").disabled = this.value !== "Multiple or Other";
              });
            });
        
            document.querySelectorAll('input[name="role"]').forEach(radio => {
                radio.addEventListener("change", function() {
                    document.getElementById("role_other").disabled = this.value !== "Other";
                });
            });
        
            document.querySelectorAll('input[name="school_type"]').forEach(radio => {
                radio.addEventListener("change", function() {
                    document.getElementById("school_other").disabled = this.value !== "Other";
                });
            }); 