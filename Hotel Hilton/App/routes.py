from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from App import db, bcrypt 
from App.forms import RegistrationForm, LoginForm, UserForm 
from App.models import User 
from functools import wraps 

main = Blueprint('main', __name__)


def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Por favor, inicia sesión para acceder a esta página.', 'info')
                return redirect(url_for('main.login'))
            if current_user.rol != role:
                flash('No tienes permiso para acceder a esta página.', 'danger')
                abort(403)   
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@main.route("/")
@main.route("/home")
def home():
    return render_template("home.html", title='Inicio')

@main.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password, rol='admin') 
        db.session.add(user)
        db.session.commit()

        flash('¡Tu cuenta ha sido creada exitosamente! Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('main.login')) 
    
    return render_template('registro.html', title='Registro', form=form)

@main.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember_me.data)
            if user.rol == 'admin':
                flash(f'¡Bienvenido administrador, {user.username}!', 'success')
                return redirect(url_for('main.dashboard_admin'))
            else:
                next_page = request.args.get('next')
                flash(f'¡Bienvenido, {user.username}!', 'success')
                return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Inicio de sesión fallido. Por favor, verifica tu email y contraseña.', 'danger')
    
    return render_template('login.html', title='Iniciar Sesión', form=form)

@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('main.home'))


@main.route("/dashboard_admin")
@login_required
@role_required('admin') 
def dashboard_admin():
    users = User.query.all() 
    return render_template('dashboard_admin.html', title='Dashboard Admin', users=users)

@main.route("/user/new", methods=['GET', 'POST'])
@login_required
@role_required('admin')  
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        if not form.password.data:
            flash('La contraseña es obligatoria para crear un nuevo usuario.', 'danger')
            return render_template('usuarios/formulario_usuario.html', title='Crear Usuario', form=form)

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password, rol=form.rol.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Usuario "{user.username}" creado exitosamente!', 'success')
        return redirect(url_for('main.dashboard_admin'))
    
    return render_template('usuarios/formulario_usuario.html', title='Crear Usuario', form=form)

@main.route("/user/<int:user_id>/edit", methods=['GET', 'POST'])
@login_required
@role_required('admin') 
def edit_user(user_id):
    user = User.query.get_or_404(user_id) 
    form = UserForm()

    if form.validate_on_submit():
       
        user.username = form.username.data
        user.email = form.email.data
        user.rol = form.rol.data
        
        
        if form.password.data:
            user.password_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        db.session.commit()
        flash(f'Usuario "{user.username}" actualizado exitosamente!', 'success')
        return redirect(url_for('main.dashboard_admin'))
    elif request.method == 'GET':
       
        form.id_usuario.data = user.id_usuario 
        form.username.data = user.username
        form.email.data = user.email
        form.rol.data = user.rol
    
    return render_template('usuarios/formulario_usuario.html', title='Editar Usuario', form=form)

@main.route("/user/<int:user_id>/delete", methods=['POST'])
@login_required
@role_required('admin') 
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if current_user.id_usuario == user_id:
        flash('No puedes eliminar tu propia cuenta de administrador desde aquí.', 'danger')
        return redirect(url_for('main.dashboard_admin'))

    db.session.delete(user)
    db.session.commit()
    flash(f'Usuario "{user.username}" eliminado exitosamente!', 'success')
    return redirect(url_for('main.dashboard_admin'))