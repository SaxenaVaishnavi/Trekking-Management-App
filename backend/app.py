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
    

@app.route('/api/trekker/dashboard', methods=['GET'])
@jwt_required()
def trekker_dashboard():
    user_id = get_jwt_identity()

    upcoming = (
        Booking.query
        .filter_by(user_id=user_id, booking_status='booked')
        .join(Trek)
        .order_by(Trek.start_date.asc())
        .limit(3)
        .all()
    )

    recent_bookings = []
    for b in upcoming:
        recent_bookings.append({
            'booking_id': b.id,
            'trek_name': b.trek.name,
            'booking_date': b.booking_date.strftime('%d %b %Y'),
            'trek_dates': f"{b.trek.start_date.strftime('%d %b')} - {b.trek.end_date.strftime('%d %b %Y')}",
            'status': b.booking_status
        })

    available_treks = Trek.query.filter_by(status='open').limit(3).all()
    treks_data = []
    for t in available_treks:
        treks_data.append({
            'id': t.id,
            'name': t.name,
            'location': t.location,
            'difficulty': t.difficulty,
            'duration': t.duration,
            'available_slots': t.available_slots
        })

    return jsonify({'data': {
        'available_treks': treks_data,
        'recent_bookings': recent_bookings
    }}), 200


@app.route('/api/staff/dashboard', methods=['GET'])
@jwt_required()
def staff_dashboard():
    staff_id = get_jwt_identity()
    staff = User.query.get(staff_id)

    if staff.role != 'staff':
        return jsonify({'message': 'Access denied'}), 403

    assigned_treks = Trek.query.filter_by(assigned_staff_id=staff_id).all()

    total_participants = 0
    ongoing_treks = 0
    treks_data = []

    for t in assigned_treks:
        participant_count = Booking.query.filter_by(trek_id=t.id, booking_status='booked').count()
        total_participants += participant_count
        if t.status == 'open':
            ongoing_treks += 1

        treks_data.append({
            'id': t.id,
            'name': t.name,
            'dates': f"{t.start_date.strftime('%d %b')} - {t.end_date.strftime('%d %b %Y')}",
            'participants': participant_count,
            'total_slots': t.total_slots,
            'status': t.status
        })

    return jsonify({'data': {
        'kpis': {
            'assigned_treks': len(assigned_treks),
            'total_participants': total_participants,
            'ongoing_treks': ongoing_treks
        },
        'assigned_treks': treks_data
    }}), 200


@app.route('/api/admin/dashboard', methods=['GET'])
@jwt_required()
def admin_dashboard():
    admin_id = get_jwt_identity()
    admin = User.query.get(admin_id)

    if admin.role != 'admin':
        return jsonify({'message': 'Access denied'}), 403

    total_treks = Trek.query.count()
    total_trekkers = User.query.filter_by(role='trekker').count()
    total_staff = User.query.filter_by(role='staff').count()
    total_bookings = Booking.query.count()

    recent = Booking.query.order_by(Booking.booking_date.desc()).limit(5).all()
    recent_bookings = []
    for b in recent:
        recent_bookings.append({
            'booking_id': b.id,
            'trekker_name': f"{b.user.fname} {b.user.lname}",
            'trek_name': b.trek.name,
            'booking_date': b.booking_date.strftime('%d %b %Y'),
            'status': b.booking_status
        })

    return jsonify({'data': {
        'kpis': {
            'total_treks': total_treks,
            'total_trekkers': total_trekkers,
            'total_staff': total_staff,
            'total_bookings': total_bookings
        },
        'recent_bookings': recent_bookings
    }}), 200


# ===================================================================================
# ===================================================================================

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