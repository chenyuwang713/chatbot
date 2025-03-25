from flask import Blueprint, request, jsonify, make_response, render_template
from flask_cors import cross_origin
from models import db, User, Survey, Admin, Chat
import hashlib
from openai import OpenAI
import os
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

routes = Blueprint('routes', __name__)

bcrypt = Bcrypt()
jwt = JWTManager()

client = OpenAI(api_key=os.getenv('LLM_API_KEY'))

prompt_template = (
    "You are an agent that interacts with an interviewee to evaluate the interviewee's Education Leaders' Personality traits. The tone should be natrual and profesional.\n\n "
    "Here are some instructions you should follow:\n\n"
    "(a) Begin with an initial screening and rapport building process by asking the interviewee about the details of interviewee's leader's role in education. "
    "(b) Courteously ask them to provide as much information as possible. If the role and responsibility are not correctly or clearly elicited, please stay politely to inquire until secure them.\n\n"
    "(c) If we have understood their role, conduct a natural conversation to assess the dark traits of [Narcissism], [Machiavellianism], [Psychopathy] across the following 27 points. The 27 points are:\n"
    "1. I have a natural talent for influencing people. [Narcissism]\n"
    "2. I am not good at influencing people. (Reverse-scored) [Narcissism]\n"
    "3. Modesty doesn't become me. [Narcissism]\n"
    "4. I would do anything on a dare. [Narcissism]\n"
    "5. I tend to expect special favors from others. [Narcissism]\n"
    "6. I insist on getting the respect I deserve. [Narcissism]\n"
    "7. I like to show off my body. [Narcissism]\n"
    "8. I can read people like a book. [Narcissism]\n"
    "9. People always seem to recognize my authority. [Narcissism]\n"
    "10. I like to use clever manipulation to get my way. [Machiavellianism]\n"
    "11. I don't particularly like to manipulate people. (Reverse-scored) [Machiavellianism]\n"
    "12. I feel bad if my words or actions cause someone else to feel emotional pain. (Reverse-scored) [Machiavellianism]\n"
    "13. Whatever it takes, you must get the important people on your side. [Machiavellianism]\n"
    "14. Avoid direct conflict with others because they may be useful in the future. [Machiavellianism]\n"
    "15. It's wise to keep track of information that you can use against people later. [Machiavellianism]\n"
    "16. You should wait for the right time to get back at people. [Machiavellianism]\n"
    "17. There are things you should hide from other people to preserve your reputation. [Machiavellianism]\n"
    "18. Make sure your plans benefit you, not others. [Machiavellianism]\n"
    "19. People who mess with me always regret it. [Psychopathy]\n"
    "20. I have been compared to famous historical figures. [Psychopathy]\n"
    "21. I like to get revenge on authorities. [Psychopathy]\n"
    "22. I avoid dangerous situations. (Reverse-scored) [Psychopathy]\n"
    "23. Payback needs to be quick and nasty. [Psychopathy]\n"
    "24. I enjoy having sex with people I hardly know. [Psychopathy]\n"
    "25. I often get others to pay for my expenses. [Psychopathy]\n"
    "26. I'll say anything to get what I want. [Psychopathy]\n"
    "27. I would be upset if my success came at someone else's expense. (Reverse-scored) [Psychopathy]\n\n"
    "(d) Use the format '[Intro to the Point] [Point]' to present them.\n\n"
    "(e) Ask the interviewee to rate each [Point] on a Likert scale from 1 (strongly disagree) to 5 (strongly agree), and indicate this rule in each [Point].\n\n"
    "(f) If the interviewee does not respond a number rating (1-5) to any [Point] or if you could not infer the numeric rating, continue to prompt them UNTIL they input the number regarding that [Point].\n\n"
    "(g) Each [Intro to the point] should be brief (under 100 words) with an envisoned senario that might be associated with the interviewee, and should be phrased to associated with [Interviewee's role], and [Point] should be associated with [Intro to the point]\n\n"
    "(h) Check if any [Point] among the 27 points is missing to assess in the conversation, and repeat to do so untill all points have been assessed.\n\n"
    "(i) Do not repeatedly acquire the educational role, only acquiring the role at the start of the conversion.\n\n"
    "(j) After completing all 27 [Point], conclude the interview with [END OF INTERVIEW].\n\n"
    "(k) Do not label any [Point] with number when asking interviewee the question.\n\n"
    "(l) When making [Intro to the point], Please do not describe it with general phrase such as 'in your education setting', please associate it with the interviewee's role.\n\n "

    "[Start to interview]"
)

def hash_email(email):
    return hashlib.sha256(email.encode()).hexdigest()


from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from models import db, User
from flask_jwt_extended import jwt_required

routes = Blueprint('routes', __name__)

@routes.route('/user/status', methods=['GET'])
def check_user_status():
    """Check the user's agreement, survey completion, and chat history status."""
    uid = request.args.get("uid")
    if not uid:
        return jsonify({"error": "Missing UID"}), 400
    
    user = User.query.filter_by(identifier=uid).first()
    if not user:
        return jsonify({"error": "Invalid UID"}), 400  
    
    if not user.consent_given:
        return jsonify({"redirect": f"consent.html?uid={uid}"}), 200  


    survey_record = Survey.query.filter_by(uid=uid).first()
    chat_history = Chat.query.filter_by(identifier=uid).order_by(Chat.timestamp.asc()).all()
    completed_chat = Chat.query.filter_by(identifier=uid, sender="system", content="[END OF INTERVIEW]").first()

    if not survey_record:
        return jsonify({"redirect": f"survey.html?uid={uid}"}), 200  # Redirect to survey if not completed
    elif completed_chat:
        return jsonify({"redirect": "complete.html"}), 200  # Redirect to completion page
    elif not chat_history:
        return jsonify({"redirect": f"chat.html?uid={uid}"}), 200  # Start AI conversation
    else:
        return jsonify({"redirect": f"chat.html?uid={uid}"}), 200  # Load chat history

@routes.route('/upload_emails', methods=['POST'])
@cross_origin(origin='http://localhost:3001', supports_credentials=True)
@jwt_required()
def upload_emails():
    """Handle email uploads and store them in the database."""
    try:
        data = request.get_json()
        if not data or "users" not in data:
            return jsonify({"error": "Invalid request format"}), 400

        users = data["users"]
        added_users = []

        for user in users:
            if "email" not in user or "identifier" not in user:
                return jsonify({"error": "Missing email or identifier"}), 400

            # Check for duplicate email
            existing_user = User.query.filter_by(email=user["email"]).first()
            if not existing_user:
                new_user = User(email=user["email"], identifier=user["identifier"])
                db.session.add(new_user)
                added_users.append({"email": user["email"], "identifier": user["identifier"]})

        db.session.commit()
        return jsonify({"message": "Emails uploaded successfully", "uploaded_users": added_users}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
@routes.route('/get_uploaded_emails', methods=['GET'])
@cross_origin(origin='http://localhost:3001', supports_credentials=True)
@jwt_required()
def get_uploaded_emails():
    """Retrieve all uploaded emails from the database."""
    try:
        users = User.query.all()
        user_list = [{"email": user.email, "identifier": user.identifier} for user in users]
        return jsonify({"users": user_list}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@routes.route('/submit_survey', methods=['POST'])
@cross_origin(origin='http://localhost:8080', supports_credentials=True)
def submit_survey():
    """Store survey responses in the database."""
    try:
        data = request.get_json()

        required_fields = ["uid", "race", "gender", "role", "experience", "school_type", "ai_usage"]
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        # Ensure UID is not null
        if not data["uid"]:
            return jsonify({"error": "UID is missing from the request"}), 400

        new_survey = Survey(
            uid=data["uid"],
            race=data["race"],
            race_other=data.get("race_other", ""),
            gender=data["gender"],
            role=data["role"],
            role_other=data.get("role_other", ""),
            experience=data["experience"],
            school_type=data["school_type"],
            school_other=data.get("school_other", ""),
            ai_usage=data["ai_usage"]
        )

        db.session.add(new_survey)
        db.session.commit()

        return jsonify({"message": "Survey submitted successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@routes.route('/chat_history', methods=['GET'])
def get_chat_history():
    max_sends = 50
    uid = request.args.get("uid")
    if not uid:
        return jsonify({"error": "Missing UID"}), 400
    
    user_message_count = Chat.query.filter_by(identifier=uid, sender="user").count()
    remaining_sends = max_sends - user_message_count
    
    # Retrieve all chat records for this UID
    chat_records =  Chat.query.filter(Chat.identifier == uid, Chat.sender != "system").order_by(Chat.timestamp.asc()).all()
    
    # Build a JSON-friendly list
    conversation = []
    for record in chat_records:
        conversation.append({
            "sender": record.sender,
            "content": record.content
        })

    return jsonify({"conversation": conversation, "remaining_sends": remaining_sends}), 200

@routes.route('/chat', methods=['POST'])
@cross_origin(origin='http://localhost:3001', supports_credentials=True)
def chat():

    max_sends = 50
    data = request.json
    message = request.json.get("message")
    uid = request.json.get("uid")
    if not uid:
        return jsonify({"error": "UID is missing from the request"}), 400
    
    # 1) Fetch conversation so far
    chat_history = Chat.query.filter_by(identifier=uid).order_by(Chat.timestamp.asc()).all()
    conversation_history = [
        {"role": ch.sender, "content": ch.content} for ch in chat_history
    ]
    
    
    # If no history exists, initialize with the prompt template
    if  len(conversation_history)==0:
        # 1) Add the system message to DB

        # 2) Get the initial assistant message from OpenAI
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": prompt_template}],
                max_tokens=500
            )
            initial_ai_response = response.choices[0].message.content
        except Exception as e:
            initial_ai_response = f"Error: {str(e)}"

        system_msg = Chat(identifier=data["uid"], sender="system", content=prompt_template)
        db.session.add(system_msg)
        assistant_msg = Chat(identifier=data["uid"], sender="assistant", content=initial_ai_response)
        db.session.add(assistant_msg)
        db.session.commit()

        user_message_count = Chat.query.filter_by(identifier=uid, sender="user").count()
        remaining_sends = max_sends - user_message_count

        return jsonify({"assistant": initial_ai_response, "remaining_sends": remaining_sends}), 200
    
    if request.method == "POST" and message!="":

        user_message_count = Chat.query.filter_by(identifier=uid, sender="user").count()
        remaining_sends = max_sends - user_message_count
        if remaining_sends <= 0 :
            return jsonify({"error": "You have reached the maximum number of messages allowed."}), 400

        user_msg = Chat(identifier=data["uid"], sender="user", content=message)
        db.session.add(user_msg)
        db.session.commit()
        conversation_history.append({"role": "user", "content": message})
        try:
            response = client.chat.completions.create(
                model="gpt-4o", 
                messages=conversation_history,
                max_tokens=500
            )
            ai_response = response.choices[0].message.content
        except Exception as e:
            ai_response = f"Error: {str(e)}"
        
        # Record the AI's response in the database
        ai_msg = Chat(identifier=data["uid"], sender="assistant", content=ai_response)
        db.session.add(ai_msg)
        db.session.commit()
        conversation_history.append({"role": "assistant", "content": ai_response})

        user_message_count = Chat.query.filter_by(identifier=uid, sender="user").count()
        remaining_sends = max_sends - user_message_count
        
        return jsonify({"user": message, "assistant": ai_response, "remaining_sends": remaining_sends}), 200
    
    return jsonify({"remaining_sends": remaining_sends}), 200
    
    

@routes.route('/admin/register', methods=['POST'])
def admin_register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if Admin.query.filter_by(email=email).first():
        return jsonify({'error': 'Admin already exists'}), 400
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_admin = Admin(email=email, password_hash=hashed_password)
    db.session.add(new_admin)
    db.session.commit()
    return jsonify({'message': 'Admin registered successfully'}), 201

@routes.route('/admin/login', methods=['POST', 'OPTIONS'])
@cross_origin(origin='http://localhost:3001', supports_credentials=True)
def admin_login():
    if request.method == 'OPTIONS':  # Handle preflight request
        response = make_response()
        response.headers["Access-Control-Allow-Origin"] = "http://localhost:3001"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response, 200
    
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    admin = Admin.query.filter_by(email=email).first()
    if not admin or not bcrypt.check_password_hash(admin.password_hash, password):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    access_token = create_access_token(identity=admin.email)
    return jsonify({'access_token': access_token}), 200


@routes.route('/delete_user', methods=['DELETE', 'OPTIONS'])
@cross_origin(origin='http://localhost:3001', supports_credentials=True)
def delete_user():
    """Delete a user by UID."""
    # Handle preflight request
    if request.method == "OPTIONS":
        response = make_response()
        response.headers["Access-Control-Allow-Origin"] = "http://localhost:3001"
        response.headers["Access-Control-Allow-Methods"] = "DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response, 200

    uid = request.args.get("uid")

    if not uid:
        return jsonify({"error": "Missing UID"}), 400

    user = User.query.filter_by(identifier=uid).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
    
@routes.route('/update_consent', methods=['POST'])
@cross_origin(origin='http://localhost:3001', supports_credentials=True)
def update_consent():
    
    data = request.json
    uid = data.get('uid')

    if not uid:
        return jsonify({"success": False, "message": "Missing UID"}), 400

    # Find the user by UID
    user = User.query.filter_by(identifier=uid).first()

    if user:
        user.consent_given = True 
        db.session.commit()
        return jsonify({"success": True, "message": "Consent updated successfully!"})
    
    return jsonify({"success": False, "message": "User not found"}), 404