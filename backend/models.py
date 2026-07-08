from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(20), nullable=False, default='trekker')   # 'admin', 'staff', 'trekker'
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    fname = db.Column(db.String(30), nullable=True)
    lname = db.Column(db.String(30), nullable=True)
    age = db.Column(db.Integer, nullable=False)           # A trek staff must be at least 21 years old while a trekker's age depends on the trek's age limit.
    language = db.Column(db.String(30), nullable=True)   # This is the priamry language of the user. It can be used to filter treks based on language preference.
    phone = db.Column(db.String(15), nullable=True)
    email = db.Column(db.String(50), unique=True, nullable=False)

    # Relationship
    assigned_treks = db.relationship('Trek', backref='assigned_staff', lazy=True)  # For staff members, this is list of treks they are assigned to.
    bookings = db.relationship('Booking', backref='user', lazy=True)  # For trekkers, this is list of bookings they have made.

class Trek(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assigned_staff_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=True)  # A trek can (or cannot) be assigned to a staff member.

    name = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    end_date = db.Column(db.Date, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # in days
    length = db.Column(db.Float, nullable=False)  # in kilometers
    difficulty = db.Column(db.String(20), nullable=False)  # 'easy', 'moderate', 'difficult'
    status = db.Column(db.String(20), nullable=False, default='open')  # 'open', 'sold_out', 'completed'
    min_age = db.Column(db.Integer, nullable=False)  # Minimum age required to book the trek.
    max_age = db.Column(db.Integer, nullable=False)  # Maximum age allowed to book the trek.

    total_slots = db.Column(db.Integer, nullable=False)
    available_slots = db.Column(db.Integer, nullable=False)  # At the time of trek creation, available_slots = total_slots. When available_slots = 0, the trek's status will be updated to 'sold_out'.
    price = db.Column(db.Float, nullable=False)

    # Relationship
    bookings = db.relationship('Booking', backref='trek', lazy=True)  # List of bookings for a trek.
    # an attribute `assigned_staff` would be available to access the staff member assigned to the trek.

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey(Trek.id), nullable=False)

    booking_date = db.Column(db.DateTime, nullable=False)
    payment_status = db.Column(db.String(20), nullable=False, default='pending')  # 'pending', 'successful', 'failed'
    booking_status = db.Column(db.String(20), nullable=False, default='booked')   # 'booked' - when payment received, 'cancelled' - if cancelled by the user, 'completed' - when trek is completed.

    # Relationship
    # an attribute `user` would be available to access the user who made the booking.
    # an attribute `trek` would be available to access the trek for which the booking was made.