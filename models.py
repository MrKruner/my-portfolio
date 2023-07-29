from . import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    date_joined = db.Column(db.DateTime)
    access_code_id = db.Column(db.Integer, db.ForeignKey('access_code.id'), nullable=True)
    access_code = db.relationship('AccessCode', backref='users', lazy=True, foreign_keys=[access_code_id])
    messages = db.relationship('Message', backref='user', lazy=True)
    rooms = db.relationship('Room', secondary='user_room', backref='users', lazy=True)
    is_leader = db.Column(db.Boolean, default=False)

    
    
class Project(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    projectName = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    datePost = db.Column(db.DateTime, default=func.now())
    endDate = db.Column(db.DateTime, nullable=False)
    process = db.Column(db.String, nullable=False)
    
    # Foreign key relationship with User model for the author
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    author = db.relationship('User', backref = 'projects', foreign_keys=[author_id])
    
    access_code_id = db.Column(db.Integer, db.ForeignKey('access_code.id'), nullable=False)
    
    # Foreign key relationship with User model for the leader
    leader_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    leader = db.relationship('User', backref='leader_projects', foreign_keys=[leader_id])

    # Many-to-many relationship with User model for members
    members = db.relationship('User', secondary='project_member', backref='projects_joined')
    
project_member = db.Table(
    'project_member',
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)    

class Task(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    endDate = db.Column(db.DateTime, nullable=False)
    
    # Process of the tasks
    is_complete = db.Column(db.Boolean, default=False)
    
    #task giver relationship
    task_giver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    task_giver = db.relationship('User', backref = 'tasks_given')
    
    access_code_id = db.Column(db.Integer, db.ForeignKey('access_code.id'), nullable=False)
    
    #task assign relationship
    employees_task = db.relationship('User', secondary='task_employee' ,backref = 'task_assigned')
    
    
task_employee = db.Table(
    'task_employee',
    db.Column('task_id' ,db.Integer, db.ForeignKey('task.id'), primary_key = True),
    db.Column('user_id' , db.Integer, db.ForeignKey('user.id'), primary_key = True)
)
    
class AccessCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    projects = db.relationship('Project', backref='access_code', lazy=True)
    tasks = db.relationship('Task', backref='access_code', lazy=True)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)

    # Relationships
    room = db.relationship('Room', backref='messages', lazy=True)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    code = db.Column(db.String(10), unique=True)
    access_code_id = db.Column(db.Integer, db.ForeignKey('access_code.id'), nullable=False)
    

user_room = db.Table('user_room',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('room_id', db.Integer, db.ForeignKey('room.id'), primary_key=True)
)