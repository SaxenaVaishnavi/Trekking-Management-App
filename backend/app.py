from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, User, Trek, Booking
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from functools import wraps
from datetime import datetime


app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trekking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = '23f2003009'  # My IITM roll no

# Initialize extensions
CORS(app)
db.init_app(app)
jwt = JWTManager(app)


# ====================================================================================
#                                       ROUTES 
# ====================================================================================

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

    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'message': 'Invalid username or password'}), 401
    
    if not user.is_active:
        return jsonify({'message': 'Your account has been deactivates. Please contact admin.'}), 403
    
    access_token = create_access_token(identity=str(user.id))
    return jsonify({'message': 'Login successful', 
                    'data': {
                        'username': user.username,
                        'email': user.email,
                        'phone': user.phone,
                        'role': user.role,
                        'age': user.age,
                        'language': user.language,
                        'access_token': access_token
                        }
                    }), 200


# ============================================= TREKKER ROUTES ====================================
# =================================================================================================

@app.route('/api/trekker/dashboard', methods=['GET'])
@jwt_required()
def trekker_dashboard():
    user_id = int(get_jwt_identity())

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
            'description': t.description,
            'start_date': t.start_date.isoformat(),
            'end_date': t.end_date.isoformat(),
            'duration': t.duration,
            'length': t.length,
            'difficulty': t.difficulty,
            'status': t.status,
            'min_age': t.min_age,
            'max_age': t.max_age,
            'total_slots': t.total_slots,
            'available_slots': t.available_slots,
            'price': t.price
        })

    return jsonify({'data': {
        'available_treks': treks_data,
        'recent_bookings': recent_bookings
    }}), 200


@app.route('/api/treks', methods=['GET'])
@jwt_required()
def get_treks():
    treks = Trek.query.filter_by(status='open').all()
    result = []
    for trek in treks:
        result.append({
            'id': trek.id,
            'name': trek.name,
            'location': trek.location,
            'description': trek.description,
            'start_date': trek.start_date.isoformat(),
            'end_date': trek.end_date.isoformat(),
            'duration': trek.duration,
            'length': trek.length,
            'difficulty': trek.difficulty,
            'status': trek.status,
            'min_age': trek.min_age,
            'max_age': trek.max_age,
            'total_slots': trek.total_slots,
            'available_slots': trek.available_slots,
            'price': trek.price
        })

    return jsonify({'data': result}), 200


@app.route('/api/bookings', methods=['POST'])
@jwt_required()
def create_booking():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    data = request.get_json()

    if not data or 'trek_id' not in data:
        return jsonify({'message': 'trek_id is required'}), 400

    trek = Trek.query.get(data['trek_id'])
    if not trek:
        return jsonify({'message': 'Trek not found'}), 404

    if trek.status != 'open' or trek.available_slots <= 0:
        return jsonify({'message': 'This trek is not available for booking'}), 400

    if user.age < trek.min_age or user.age > trek.max_age:
        return jsonify({'message': f'This trek requires age between {trek.min_age} and {trek.max_age}'}), 400

    existing = Booking.query.filter_by(
        user_id=user_id, trek_id=trek.id, booking_status='booked'
    ).first()

    if existing:
        return jsonify({'message': 'You have already booked this trek'}), 400

    new_booking = Booking(
        user_id=user_id,
        trek_id=trek.id,
        booking_date=datetime.utcnow(),
        payment_status='pending',
        booking_status='booked'
    )

    trek.available_slots -= 1
    if trek.available_slots == 0:
        trek.status = 'sold_out'

    db.session.add(new_booking)
    db.session.commit()

    return jsonify({'message': 'Booking successful'}), 201


@app.route('/api/my-bookings', methods=['GET'])
@jwt_required()
def get_my_bookings():
    user_id = int(get_jwt_identity())
    bookings = Booking.query.filter_by(user_id=user_id, booking_status='booked').all()

    result = []
    for b in bookings:
        trek = b.trek
        result.append({
            'booking_id': b.id,
            'trek_id': trek.id,
            'trek_name': trek.name,
            'location': trek.location,
            'start_date': trek.start_date.isoformat(),
            'end_date': trek.end_date.isoformat(),
            'price': trek.price,
            'booking_date': b.booking_date.isoformat(),
            'payment_status': b.payment_status,
            'booking_status': b.booking_status
        })
    return jsonify({'data': result}), 200


@app.route('/api/trekker/history', methods=['GET'])
@jwt_required()
def get_trekker_history():
    user_id = int(get_jwt_identity())
    bookings = (
        Booking.query
        .filter_by(user_id=user_id)
        .filter(Booking.booking_status.in_(['cancelled', 'completed', 'invalidated']))
        .order_by(Booking.booking_date.desc())
        .all()
    )

    result = []
    for b in bookings:
        trek = b.trek
        result.append({
            'booking_id': b.id,
            'trek_name': trek.name,
            'location': trek.location,
            'start_date': trek.start_date.isoformat(),
            'end_date': trek.end_date.isoformat(),
            'price': trek.price,
            'booking_status': b.booking_status
        })
    return jsonify({'data': result}), 200


@app.route('/api/trekker/profile', methods=['GET'])
@jwt_required()
def get_trekker_profile():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    return jsonify({'data': {
        'username': user.username,
        'fname': user.fname,
        'lname': user.lname,
        'email': user.email,
        'phone': user.phone,
        'age': user.age,
        'language': user.language
    }}), 200


@app.route('/api/trekker/profile', methods=['PUT'])
@jwt_required()
def update_trekker_profile():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    data = request.get_json()

    if 'email' in data and data['email'] != user.email:
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'Email already in use'}), 400

    for field in ['fname', 'lname', 'email', 'phone', 'age', 'language']:
        if field in data:
            setattr(user, field, data[field])

    db.session.commit()
    return jsonify({'message': 'Profile updated successfully'}), 200


@app.route('/api/trekker/profile/password', methods=['PUT'])
@jwt_required()
def change_trekker_password():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    data = request.get_json()

    if not data or not all(k in data for k in ('current_password', 'new_password')):
        return jsonify({'message': 'current_password and new_password are required'}), 400

    if not check_password_hash(user.password_hash, data['current_password']):
        return jsonify({'message': 'Current password is incorrect'}), 401

    user.password_hash = generate_password_hash(data['new_password'])
    db.session.commit()
    return jsonify({'message': 'Password changed successfully'}), 200



# ============================================= STAFF ROUTES ====================================
# ==============================================================================================

def staff_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = int(get_jwt_identity())
        current_user = User.query.get(user_id)
        if not current_user or current_user.role != 'staff':
            return jsonify({'message': 'Staff access required'}), 403
        return fn(*args, **kwargs)
    return wrapper


@app.route('/api/staff/dashboard', methods=['GET'])
@staff_required
def staff_dashboard():
    staff_id = int(get_jwt_identity())
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


@app.route('/api/staff/my-treks', methods=['GET'])
@staff_required
def staff_my_treks():
    staff_id = int(get_jwt_identity())
    treks = Trek.query.filter_by(assigned_staff_id=staff_id).order_by(Trek.start_date.desc()).all()

    result = []
    for t in treks:
        participant_count = Booking.query.filter_by(trek_id=t.id, booking_status='booked').count()
        result.append({
            'id': t.id,
            'name': t.name,
            'location': t.location,
            'start_date': t.start_date.isoformat(),
            'end_date': t.end_date.isoformat(),
            'status': t.status,
            'total_slots': t.total_slots,
            'available_slots': t.available_slots,
            'participant_count': participant_count
        })

    return jsonify({'data': result}), 200


# this is used by a modal
@app.route('/api/staff/treks/<int:trek_id>/participants', methods=['GET'])
@staff_required
def staff_trek_participants(trek_id):
    staff_id = int(get_jwt_identity())
    trek = Trek.query.get(trek_id)

    if not trek:
        return jsonify({'message': 'Trek not found'}), 404

    # Authorization: this trek must actually be assigned to the requesting staff member
    if trek.assigned_staff_id != staff_id:
        return jsonify({'message': 'You are not assigned to this trek'}), 403

    bookings = Booking.query.filter_by(trek_id=trek.id, booking_status='booked').all()

    participants = []
    for b in bookings:
        participants.append({
            'booking_id': b.id,
            'name': f'{b.user.fname} {b.user.lname}',
            'age': b.user.age,
            'language': b.user.language,
            'phone': b.user.phone
        })

    return jsonify({'data': {
        'trek_name': trek.name,
        'participants': participants
    }}), 200


@app.route('/api/staff/participants', methods=['GET'])
@staff_required
def staff_all_participants():
    staff_id = int(get_jwt_identity())
    treks = Trek.query.filter_by(assigned_staff_id=staff_id).all()

    result = []
    for t in treks:
        bookings = Booking.query.filter_by(trek_id=t.id, booking_status='booked').all()
        for b in bookings:
            result.append({
                'trek_name': t.name,
                'name': f'{b.user.fname} {b.user.lname}',
                'age': b.user.age,
                'language': b.user.language,
                'phone': b.user.phone
            })

    return jsonify({'data': result}), 200

@app.route('/api/staff/profile', methods=['GET'])
@staff_required
def get_staff_profile():
    staff_id = int(get_jwt_identity())
    staff = User.query.get(staff_id)
    return jsonify({'data': {
        'username': staff.username,
        'fname': staff.fname,
        'lname': staff.lname,
        'email': staff.email,
        'phone': staff.phone,
        'age': staff.age,
        'language': staff.language
    }}), 200


@app.route('/api/staff/profile', methods=['PUT'])
@staff_required
def update_staff_profile():
    staff_id = int(get_jwt_identity())
    staff = User.query.get(staff_id)
    data = request.get_json()

    if 'email' in data and data['email'] != staff.email:
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'Email already in use'}), 400

    if 'age' in data and data['age'] < 21:
        return jsonify({'message': 'Trek staff must be at least 21 years old'}), 400

    for field in ['fname', 'lname', 'email', 'phone', 'age', 'language']:
        if field in data:
            setattr(staff, field, data[field])

    db.session.commit()
    return jsonify({'message': 'Profile updated successfully'}), 200


@app.route('/api/staff/profile/password', methods=['PUT'])
@staff_required
def change_staff_password():
    staff_id = int(get_jwt_identity())
    staff = User.query.get(staff_id)
    data = request.get_json()

    if not data or not all(k in data for k in ('current_password', 'new_password')):
        return jsonify({'message': 'current_password and new_password are required'}), 400

    if not check_password_hash(staff.password_hash, data['current_password']):
        return jsonify({'message': 'Current password is incorrect'}), 401

    staff.password_hash = generate_password_hash(data['new_password'])
    db.session.commit()
    return jsonify({'message': 'Password changed successfully'}), 200


# ============================================ ADMIN ROUTES ====================================
# ==============================================================================================

# this function will wrap all admin routes and will do the jwt_required check and also user.role == admin check
def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = int(get_jwt_identity())
        current_user = User.query.get(user_id)
        if not current_user or current_user.role != 'admin':
            return jsonify({'message': 'Admin access required'}), 403
        
        return fn(*args, **kwargs)
    return wrapper


@app.route('/api/admin/dashboard', methods=['GET'])
@admin_required
def admin_dashboard():
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


@app.route('/api/admin/search', methods=['GET'])
@admin_required
def admin_search():
    search_type = request.args.get('type', 'treks')   # 'treks', 'staff', 'trekkers', 'bookings'
    q = request.args.get('q', '').strip()

    if not q:
        return jsonify({'data': []}), 200

    like_pattern = f'%{q}%'

    if search_type == 'treks':
        results = Trek.query.filter(
            db.or_(Trek.name.ilike(like_pattern), Trek.location.ilike(like_pattern))
        ).all()

        data = [{
            'id': t.id, 'name': t.name, 'location': t.location,
            'status': t.status, 'start_date': t.start_date.isoformat()
        } for t in results]

    elif search_type == 'staff':
        results = User.query.filter_by(role='staff').filter(
            db.or_(User.username.ilike(like_pattern), User.fname.ilike(like_pattern),
                   User.lname.ilike(like_pattern), User.email.ilike(like_pattern))
        ).all()

        data = [{
            'id': u.id, 'name': f'{u.fname} {u.lname}', 'username': u.username,
            'email': u.email, 'is_active': u.is_active
        } for u in results]

    elif search_type == 'trekkers':
        results = User.query.filter_by(role='trekker').filter(
            db.or_(User.username.ilike(like_pattern), User.fname.ilike(like_pattern),
                   User.lname.ilike(like_pattern), User.email.ilike(like_pattern))
        ).all()

        data = [{
            'id': u.id, 'name': f'{u.fname} {u.lname}', 'username': u.username,
            'email': u.email, 'is_active': u.is_active
        } for u in results]

    elif search_type == 'bookings':
        results = Booking.query.join(User).join(Trek).filter(
            db.or_(User.username.ilike(like_pattern), User.fname.ilike(like_pattern),
                   User.lname.ilike(like_pattern), Trek.name.ilike(like_pattern))
        ).all()

        data = [{
            'id': b.id, 'trekker_name': f'{b.user.fname} {b.user.lname}',
            'trek_name': b.trek.name, 'booking_status': b.booking_status,
            'booking_date': b.booking_date.isoformat()
        } for b in results]

    else:
        return jsonify({'message': 'Invalid search type'}), 400

    return jsonify({'data': data}), 200


@app.route('/api/admin/settings', methods=['GET'])
@admin_required
def admin_get_settings():
    admin_id = int(get_jwt_identity())
    admin = User.query.get(admin_id)
    return jsonify({'data': {
        'username': admin.username,
        'fname': admin.fname,
        'lname': admin.lname,
        'email': admin.email,
        'phone': admin.phone,
        'age': admin.age,
        'language': admin.language
    }}), 200


@app.route('/api/admin/settings', methods=['PUT'])
@admin_required
def admin_update_settings():
    admin_id = int(get_jwt_identity())
    admin = User.query.get(admin_id)
    data = request.get_json()

    # Prevent duplicate email if changed
    if 'email' in data and data['email'] != admin.email:
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'Email already in use'}), 400

    for field in ['fname', 'lname', 'email', 'phone', 'age', 'language']:
        if field in data:
            setattr(admin, field, data[field])

    db.session.commit()
    return jsonify({'message': 'Settings updated successfully'}), 200


@app.route('/api/admin/settings/password', methods=['PUT'])
@admin_required
def admin_change_password():
    admin_id = int(get_jwt_identity())
    admin = User.query.get(admin_id)
    data = request.get_json()

    if not data or not all(k in data for k in ('current_password', 'new_password')):
        return jsonify({'message': 'current_password and new_password are required'}), 400

    if not check_password_hash(admin.password_hash, data['current_password']):
        return jsonify({'message': 'Current password is incorrect'}), 401

    admin.password_hash = generate_password_hash(data['new_password'])
    db.session.commit()
    return jsonify({'message': 'Password changed successfully'}), 200



# ============================================== TREK CRUD ==============================================

@app.route('/api/admin/treks', methods=['POST'])
@admin_required
def admin_create_trek():
    data = request.get_json()
    required = ['name', 'location', 'start_date', 'end_date', 'duration',
                'length', 'difficulty', 'min_age', 'max_age', 'total_slots', 'price']
    
    if not data or not all(k in data for k in required):
        return jsonify({'message': 'Missing required fields'}), 400

    new_trek = Trek(
        name=data['name'],
        location=data['location'],
        description=data.get('description', ''),
        start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date(),
        end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date(),
        duration=data['duration'],
        length=data['length'],
        difficulty=data['difficulty'],
        status='open',
        min_age=data['min_age'],
        max_age=data['max_age'],
        total_slots=data['total_slots'],
        available_slots=data['total_slots'],  
        price=data['price'],
        assigned_staff_id=data.get('assigned_staff_id')
    )
    db.session.add(new_trek)
    db.session.commit()

    return jsonify({'message': 'Trek created successfully', 'id': new_trek.id}), 201


@app.route('/api/admin/treks', methods=['GET'])
@admin_required
def admin_list_treks():
    filter_status = request.args.get('status')       # ?status=open
    include_closed = request.args.get('include_closed', 'false').lower() == 'true'

    query = Trek.query
    if filter_status:
        query = query.filter_by(status=filter_status)
    elif not include_closed:
        query = query.filter(Trek.status != 'closed')

    treks = query.order_by(Trek.start_date.desc()).all()

    result = []
    for t in treks:
        result.append({
            'id': t.id,
            'name': t.name,
            'location': t.location,
            'description': t.description,
            'start_date': t.start_date.isoformat(),
            'end_date': t.end_date.isoformat(),
            'duration': t.duration,
            'length': t.length,
            'difficulty': t.difficulty,
            'status': t.status,
            'min_age': t.min_age,
            'max_age': t.max_age,
            'total_slots': t.total_slots,
            'available_slots': t.available_slots,
            'price': t.price,
            'assigned_staff_id': t.assigned_staff_id,
            'assigned_staff_name': f"{t.assigned_staff.fname} {t.assigned_staff.lname}" if t.assigned_staff else None
        })
    return jsonify({'data': result}), 200


@app.route('/api/admin/treks/<int:trek_id>', methods=['PUT'])
@admin_required
def admin_update_trek(trek_id):
    trek = Trek.query.get(trek_id)
    if not trek:
        return jsonify({'message': 'Trek not found'}), 404

    data = request.get_json()

    for field in ['name', 'location', 'description', 'duration', 'length',
                  'difficulty', 'status', 'min_age', 'max_age', 'price', 'assigned_staff_id']:
        if field in data:
            setattr(trek, field, data[field])

    if 'start_date' in data:
        trek.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
    if 'end_date' in data:
        trek.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()

    # total_slots cant be less than already-booked count
    if 'total_slots' in data:
        booked_count = Booking.query.filter_by(trek_id=trek.id, booking_status='booked').count()
        if data['total_slots'] < booked_count:
            return jsonify({'message': f'Cannot set total_slots below {booked_count} (already booked)'}), 400
        
        slots_diff = data['total_slots'] - trek.total_slots
        trek.total_slots = data['total_slots']
        trek.available_slots += slots_diff

    db.session.commit()
    return jsonify({'message': 'Trek updated successfully'}), 200


@app.route('/api/admin/treks/<int:trek_id>/close', methods=['PUT'])
@admin_required
def admin_close_trek(trek_id):
    trek = Trek.query.get(trek_id)
    if not trek:
        return jsonify({'message': 'Trek not found'}), 404

    if trek.status == 'closed':
        return jsonify({'message': 'Trek is already closed'}), 400

    trek.status = 'closed'

    # Cascade: invalidate all active bookings tied to this trek
    active_bookings = Booking.query.filter_by(trek_id=trek.id, booking_status='booked').all()
    for b in active_bookings:
        b.booking_status = 'invalidated'

    db.session.commit()
    return jsonify({'message': f'Trek closed successfully. {len(active_bookings)} booking(s) invalidated.'}), 200


@app.route('/api/admin/treks/<int:trek_id>/reopen', methods=['PUT'])
@admin_required
def admin_reopen_trek(trek_id):
    trek = Trek.query.get(trek_id)
    if not trek:
        return jsonify({'message': 'Trek not found'}), 404

    if trek.status != 'closed':
        return jsonify({'message': 'Only closed treks can be reopened'}), 400

    # Reopening doesn't restore invalidated bookings automatically — those stay invalidated
    trek.status = 'sold_out' if trek.available_slots == 0 else 'open'
    db.session.commit()
    return jsonify({'message': 'Trek reopened successfully'}), 200


# ============================================== STAFF CRUD ==============================================


@app.route('/api/admin/staff', methods=['POST'])
@admin_required
def admin_create_staff():
    data = request.get_json()
    required = ['username', 'password', 'email', 'fname', 'lname', 'age', 'phone', 'language']
    if not data or not all(k in data for k in required):
        return jsonify({'message': 'Missing required fields'}), 400

    if data['age'] < 21:
        return jsonify({'message': 'Trek staff must be at least 21 years old'}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already registered'}), 400

    new_staff = User(
        username=data['username'],
        password_hash=generate_password_hash(data['password']),
        email=data['email'],
        fname=data['fname'],
        lname=data['lname'],
        age=data['age'],
        role='staff',
        language=data['language'],
        phone=data['phone']
    )
    db.session.add(new_staff)
    db.session.commit()

    return jsonify({'message': 'Staff member created successfully'}), 201


@app.route('/api/admin/staff', methods=['GET'])
@admin_required
def admin_list_staff():
    include_inactive = request.args.get('include_inactive', 'false').lower() == 'true'

    query = User.query.filter_by(role='staff')
    if not include_inactive:
        query = query.filter_by(is_active=True)

    staff_members = query.all()

    result = []
    for s in staff_members:
        assigned_count = Trek.query.filter_by(assigned_staff_id=s.id).count()
        result.append({
            'id': s.id,
            'username': s.username,
            'fname': s.fname,
            'lname': s.lname,
            'email': s.email,
            'phone': s.phone,
            'age': s.age,
            'language': s.language,
            'is_active': s.is_active,
            'assigned_treks_count': assigned_count
        })
    return jsonify({'data': result}), 200


# Instead of deleting a staff member, we will just deactivate them. 
@app.route('/api/admin/users/<int:user_id>/status', methods=['PUT'])
@admin_required
def admin_update_user_status(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    if user.role == 'admin':
        return jsonify({'message': 'Cannot deactivate an admin account'}), 400

    data = request.get_json()
    if 'is_active' not in data:
        return jsonify({'message': 'is_active is required'}), 400

    user.is_active = data['is_active']
    cascade_message = ''

    if not user.is_active:
        if user.role == 'trekker':
            # Cascade: invalidate this trekker's active bookings
            active_bookings = Booking.query.filter_by(user_id=user.id, booking_status='booked').all()
            for b in active_bookings:
                b.booking_status = 'invalidated'
            cascade_message = f' {len(active_bookings)} booking(s) invalidated.'

        elif user.role == 'staff':
            # Cascade: unassign this staff member from their treks so treks aren't left pointing at an inactive staff member
            assigned = Trek.query.filter_by(assigned_staff_id=user.id).all()
            for t in assigned:
                t.assigned_staff_id = None
            cascade_message = f' Unassigned from {len(assigned)} trek(s).'

    db.session.commit()
    status_word = 'activated' if user.is_active else 'deactivated'
    return jsonify({'message': f'User {status_word} successfully.{cascade_message}'}), 200


# ============================================== USER CRUD ==============================================


@app.route('/api/admin/users', methods=['GET'])
@admin_required
def admin_list_users():
    include_inactive = request.args.get('include_inactive', 'false').lower() == 'true'

    query = User.query.filter_by(role='trekker')
    if not include_inactive:
        query = query.filter_by(is_active=True)

    users = query.all()

    result = []
    for u in users:
        booking_count = Booking.query.filter_by(user_id=u.id).count()
        result.append({
            'id': u.id,
            'username': u.username,
            'fname': u.fname,
            'lname': u.lname,
            'email': u.email,
            'phone': u.phone,
            'age': u.age,
            'language': u.language,
            'is_active': u.is_active,
            'total_bookings': booking_count
        })
    return jsonify({'data': result}), 200


# ============================================== BOOKINGS CRUD ==============================================

@app.route('/api/admin/bookings', methods=['GET'])
@admin_required
def admin_list_bookings():
    filter_status = request.args.get('status')   # ?status=booked
    query = Booking.query

    if filter_status:
        query = query.filter_by(booking_status=filter_status)

    bookings = query.order_by(Booking.booking_date.desc()).all()

    result = []
    for b in bookings:
        result.append({
            'id': b.id,
            'trekker_name': f"{b.user.fname} {b.user.lname}",
            'trekker_username': b.user.username,
            'trek_name': b.trek.name,
            'trek_id': b.trek.id,
            'booking_date': b.booking_date.isoformat(),
            'payment_status': b.payment_status,
            'booking_status': b.booking_status,
            'price': b.trek.price
        })
    return jsonify({'data': result}), 200


@app.route('/api/admin/bookings/<int:booking_id>/cancel', methods=['PUT'])
@admin_required
def admin_cancel_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({'message': 'Booking not found'}), 404

    if booking.booking_status != 'booked':
        return jsonify({'message': f'Cannot cancel a booking with status "{booking.booking_status}"'}), 400

    booking.booking_status = 'cancelled'

    # Give the slot back to the trek
    trek = booking.trek
    trek.available_slots += 1
    if trek.status == 'sold_out':
        trek.status = 'open'

    db.session.commit()
    return jsonify({'message': 'Booking cancelled successfully'}), 200


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