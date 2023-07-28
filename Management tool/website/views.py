from flask import Flask,flash, Blueprint, render_template, request,redirect,url_for, jsonify
from datetime import datetime
from . import db, socketio
from flask_socketio import emit,join_room, leave_room,send
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from .models import User, Project, Task, AccessCode,Room,Message

views= Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('index.html',user = current_user)

@views.route('/main/<main_code>', methods=['GET', 'POST'])
def main(main_code):
    access_code = AccessCode.query.filter_by(code=main_code).first()
    
    if access_code:
        projects = Project.query.filter_by(access_code_id=access_code.id).all()
        users = access_code.users
        
        return render_template('main.html', main_code=main_code, projects=projects, users=users, current_user=current_user)
    else:
        return redirect('/enter-code')

@views.route('/main/<main_code>/new_project', methods=['POST'])
@login_required
def new_project(main_code):
    access_code = AccessCode.query.filter_by(code=main_code).first()
    if not access_code:
        return redirect(url_for('views.main', main_code=main_code))

    if request.method == 'POST':
        projectName = request.form['projectName']
        content = request.form['content']
        leader_id = request.form['leader']
        endDate = datetime.strptime(request.form['endDate'], '%Y-%m-%d')
        
        new_project = Project(projectName=projectName, content=content,endDate=endDate, access_code_id=access_code.id, author=current_user,process='not_started',leader_id=leader_id)
        
        selected_users = request.form.getlist('users')
        
        for user_id in selected_users:
            user = User.query.get(user_id)
            if user:
                new_project.members.append(user)
        
        db.session.add(new_project)
        db.session.commit()

        return redirect(url_for('views.main', main_code=main_code))
    
@views.route('/update_project_process', methods=['POST'])
def update_project_process():
    
    project_id = request.json.get('project_id')
    new_process = request.json.get('process')

    project = Project.query.get(project_id)
    
    if project:
        project.process = new_process
        db.session.commit()
        return ''
    else: 
        return 'Project not found'

@views.route('/delete_project', methods=['POST'])
def delete_project():
    project_id = request.json.get('project_id')
    
    project = Project.query.get(project_id)
    
    if project:
        db.session.delete(project)
        db.session.commit()
        return ''
    else:
        return 'Project not found'
    
    
@views.route('/my_tasks/<main_code>')
@login_required
def my_tasks(main_code):
    access_code = AccessCode.query.filter_by(code=main_code).first()
    
    if access_code:
        users = access_code.users
        tasks = Task.query.filter_by(access_code_id=access_code.id).all()
        return render_template('myTasks.html', main_code=main_code, tasks=tasks,current_user=current_user,users=users)
    

@views.route('/my_tasks/<main_code>/new_tasks',methods=['POST'])
@login_required
def new_tasks(main_code):
    access_code = AccessCode.query.filter_by(code=main_code).first()
    if not access_code:
        return redirect(url_for('views.my_tasks', main_code=main_code))
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        endDate = datetime.strptime(request.form['endDate'], '%Y-%m-%d')
        
        
        new_task = Task(title=title, content=content,endDate=endDate,access_code_id=access_code.id,task_giver_id= current_user.id)
        
        selected_users = request.form.getlist('users')
        for user_id in selected_users:
            employee = User.query.get(user_id)
            if employee:
                new_task.employees_task.append(employee)
        
        
        db.session.add(new_task)
        db.session.commit()
        
        return redirect(url_for('views.my_tasks', main_code=main_code))
        
@views.route('/task_view_handler', methods=['POST'])
def task_view_handler():
    task_id = request.json.get('task_id')
    task = Task.query.get(task_id)
    if task:
        title= task.title
        content = task.content
        endDate = task.endDate
        
        return jsonify(title=title,content=content, endDate=endDate)
    
        
@views.route('/my_tasks/<main_code>/delete_task/<task_id>')
def delete_task(task_id, main_code):    
    task = Task.query.get(task_id)
    
    if task:
        db.session.delete(task)
        db.session.commit()

    return redirect(url_for('views.my_tasks', main_code=main_code))

@views.route('/complete_task', methods=['POST'])
def complete_task():
    task_id = request.json.get('task_id')
    main_code = request.json.get('main_code')
    
    task = Task.query.get(task_id)
    if task:
        task.is_complete = True

        db.session.commit()
        
    flash('Task completed successfully', category='success')
    return redirect(url_for('views.my_tasks', main_code=main_code))

@views.route('/my_tasks/<main_code>/undo_completed_task/<task_id>')
def undo_completed_task(task_id, main_code):
    task = Task.query.get(task_id)
    
    if task:
        task.is_complete = False
        
        db.session.commit()
        flash('Task Undo', category='success')
        return redirect(url_for('views.my_tasks', main_code=main_code))
       
    flash('Task Undo', category='error')
    return redirect(url_for('views.my_tasks', main_code=main_code))


@views.route('/members/<main_code>')
@login_required
def members(main_code):
    access_code = AccessCode.query.filter_by(code=main_code).first()
    
    if access_code:
        members = User.query.filter_by(access_code_id=access_code.id).order_by(User.date_joined.desc()).all()
        managers = User.query.filter_by(access_code_id=access_code.id, role='manager').all()
        employees = User.query.filter_by(access_code_id=access_code.id, role='employee').order_by(User.date_joined.asc()).all()
        
        return render_template('members.html', main_code=main_code, members=members,
                               current_user=current_user, managers=managers,employees=employees)
    
      
import secrets
import string

def generate_access_code(length=5):
    characters = string.ascii_letters + string.digits
    access_code = ''.join(secrets.choice(characters) for _ in range(length))
    return access_code

@views.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        existing_user = User.query.filter_by(email=email).first()
        existing_username = User.query.filter_by(username=username).first()

        code = request.form['code']
        join = request.form.get('join', False)
        create = request.form.get('create', False)

        if existing_user:
            flash('Email address already exists!', category='error')
            return redirect(url_for('views.signup'))
        elif existing_username:
            flash('Username already exists!', category='error')
            return redirect(url_for('views.signup'))
        elif join!=False:
            hashed_password = generate_password_hash(password, method='sha256')
            access_code_model = AccessCode.query.filter_by(code=code).first()
            if access_code_model:
                new_user = User(username=username, email=email, password=hashed_password, role=role,
                                date_joined = datetime.now(),access_code=access_code_model)
                db.session.add(new_user)
                db.session.commit()
                flash('Your account has been created! Joining a room...', category='success')
                user = User.query.filter_by(email=email).first()
                login_user(user, remember=True)
                return redirect(url_for('views.main', main_code=code))
            else:
                flash('Invalid code', category='error')
                return redirect(url_for('views.signup'))
            
        elif create!= False:
            hashed_password = generate_password_hash(password, method='sha256')
            code = generate_access_code()
            new_access_code = AccessCode(code=code)
            db.session.add(new_access_code)
            db.session.commit()
            access_code_model = AccessCode.query.filter_by(code=code).first()
            new_user = User(username=username, email=email, password=hashed_password, role=role,
                            date_joined = datetime.now(),access_code=access_code_model)
            db.session.add(new_user)
            db.session.commit()
            flash('Your account and room have been created!', category='success')
            user = User.query.filter_by(email=email).first()
            login_user(user, remember=True)
            return redirect(url_for('views.main', main_code=code))
        
        else:
            flash('Code needed' , category='error')

    return render_template('signup.html')


@views.route('/login', methods=["GET","POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        code = request.form['code']
        join = request.form.get('join', False)
        create = request.form.get('create', False)
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            
            
            
            if join!=False:
                access_code_model = AccessCode.query.filter_by(code=code).first()
                if access_code_model:
                    
                    user.access_code = access_code_model
                    user.date_joined = datetime.now()
                    
                    db.session.commit()
                    
                    flash('You has joined a room...', category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('views.main', main_code=code))
                else:
                    flash('Invalid code', category='error')
                    return redirect(url_for('views.login'))
                
            elif create!= False:
                code = generate_access_code()
                new_access_code = AccessCode(code=code)
                db.session.add(new_access_code)
                db.session.commit()
                access_code_model = AccessCode.query.filter_by(code=code).first()
                
                user.access_code = access_code_model
                user.date_joined = datetime.now()
                
                db.session.commit()
                
                flash('Your room have been created!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.main', main_code=code))
            
            
        
        else:
            flash("You have enter email or password incorrectly!",category='error')
            return redirect(url_for('views.login'))
        
    return render_template('login.html')

@views.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.index'))


# Chat box
@views.route('/chat/<main_code>')
@login_required
def chat(main_code):
    access_code = AccessCode.query.filter_by(code=main_code).first()
    rooms = Room.query.filter_by(access_code_id=access_code.id).all()

    if access_code:
        rooms = Room.query.filter_by(access_code_id=access_code.id).all()
        user_rooms = [room for room in rooms if current_user in room.users]
        return render_template('chat.html', rooms=user_rooms, main_code=main_code)
    
    
    return "Error, please try again later and report for us to fix your problem"

@views.route('/room/<main_code>/<room_code>')
def room(room_code, main_code):
    access_code = AccessCode.query.filter_by(code=main_code).first()
    current_room = Room.query.filter_by(code=room_code).first()
    
    if access_code:
        # Display all user's rooms
        rooms = Room.query.filter_by(access_code_id=access_code.id).all()
        user_rooms = [room for room in rooms if current_user in room.users]
        
        messages = Message.query.filter_by(room_id=current_room.id).all()
        
        return render_template('room.html',messages=messages, rooms=user_rooms, main_code=main_code, room_code=room_code)
    
    
    return "Error, please try again later and report for us to fix your problem"


@socketio.on('create_room')
def create_room(data):
    room_name = data['room_name']
    room_code = generate_access_code()
    main_code = data['main_code']

    access_code = AccessCode.query.filter_by(code=main_code).first()
    existing_room = Room.query.filter_by(name=room_name).first()
    
    if existing_room:
        emit('room_creation_failed', {'message': 'Room name already exists'})
        
    else:
        room = Room(name=room_name, code = room_code,access_code_id=access_code.id,users= [current_user])
        db.session.add(room)
        db.session.commit()


@views.route('/join_room_check/<main_code>/<room_code>')
def join_room_check(room_code, main_code):
    room= Room.query.filter_by(code=room_code).first()
    
    if room:
        room.users.append(current_user)
        db.session.commit()
        return redirect(url_for('views.room', room_code=room_code, main_code=main_code))
    else:
        return redirect(url_for('views.chat', main_code=main_code))

@socketio.on('connect')
def connect(auth):
    room_code = request.args.get('room_code')
    room = Room.query.filter_by(code = room_code).first()
    
    if not room:
        return emit('room_not_found', {'message':'Action successful'})
    
    current_user.room = room
    db.session.commit()
    
    join_room(room_code)
    emit('message', {"name": current_user.username, "message": 'has joined room'}, room=room_code)



@socketio.on('handle_join_room')
def handle_join_room(data):
    main_code = data['main_code']
    room_code = data['room_code']

    room = Room.query.filter_by(code= room_code).first()
    
    if not room:
        emit('room_not_found', {'message': 'Room not found'})

    else: 
        emit('redirect_to_join_room_check', {'main_code': main_code, 'room_code': room_code})


@socketio.on('leave_room')
def leave_room(data):
    room_id = data['room_id']
    leave_room(room_id)
    emit('room_left', {'room_id': room_id})


@socketio.on('message')
def message(data):
    room_code = data['room_code']
    message = data['message']
    
    room = Room.query.filter_by(code=room_code).first()
    
    message_db = Message(content = message, user_id=current_user.id, room_id=room.id)
    db.session.add(message_db)
    db.session.commit()
    
    emit('message', {'name': current_user.username, 'message': message, 'timestamp' : message_db.timestamp.isoformat()}, room=room_code)

