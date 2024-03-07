from flask_login import UserMixin
from werkzeug.security import check_password_hash
from sqlalchemy.sql import func
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(250), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class_enrollment = db.Table('class_enrollment',
    db.Column('class_id', db.Integer, db.ForeignKey('class.id'), primary_key=True),
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True)
)

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('classes', lazy=True))
    # New many-to-many relationship using association table
    students = db.relationship('Student', secondary=class_enrollment, backref=db.backref('classes', lazy=True))


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.String(100), nullable=False)  # Removed unique=True
    group = db.Column(db.String(50), nullable=False)
    # Removed class_id ForeignKey, relationship is handled via association table now
    participations = db.relationship('Participation', backref='student', lazy=True)


class Participation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    remarks = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime(timezone=True), server_default=func.now())
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
