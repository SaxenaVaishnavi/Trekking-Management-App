from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, User, Trek, Booking
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trekking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = '23f2003009'  # My IITM roll no

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)
CORS(app)


# ================================== Routes ==================================

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()

    # All fields not filled
    if not data or not all(k in data for k in ('username', 'password', 'email', 'age')):
        return jsonify({'message': 'Missing required fields'}), 400
    
    # Check if username already exists
    if User.query.filter_by(username=data['username']).first():
         return jsonify({'message': 'Username already exists. Choose another one.'}), 400

    # Check if email already exists (this means the user is already registered)
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'This email is already registered. Please login.'}), 400

    # Create new user
    password_hash = generate_password_hash(data['password'])
    new_user = User(
        username=data['username'],
        password_hash=password_hash,
        email=data['email'],
        fname=data['fname'],
        lname=data['lname'],
        age=data['age'],
        role=data['role'],
        language=data['language'],
        phone=data['phone']
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()

    # All fields not filled
    if not data or not all(k in data for k in ('username', 'password')):
        return jsonify({'message': 'Missing required fields'}), 400

    user = User.query.filter_by(username=data['username']).first()

    if user and check_password_hash(user.password_hash, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({'message': 'Login successful', 'data': {'username': user.username,
                                                                'email': user.email,
                                                                'phone': user.phone,
                                                                'role': user.role,
                                                                'age': user.age,
                                                                'language': user.language,
                                                                'access_token': access_token}}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401
    

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 

        # Creating Admin if not existing already
        if not User.query.filter_by(username='admin').first():
            admin_user = User(
                username='admin',
                password_hash=generate_password_hash('admin'),
                email='admin@gmail.com',
                fname='Admin',
                lname='User',
                age=30,
                role='admin',
                language='English',
                phone='1234567890'
            )
            db.session.add(admin_user)
            db.session.commit()
            
    app.run(debug=True)