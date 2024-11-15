from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.auth import auth_bp
from app.models.user import User
from app import db, limiter, csrf
from datetime import datetime

@auth_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))
        
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and user.check_password(request.form.get('password')):
            login_user(user, remember=request.form.get('remember_me'))
            user.last_login = datetime.utcnow()
            db.session.commit()
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('core.index'))
        flash('Invalid username or password', 'error')
    
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
@limiter.limit("3 per hour")
def register():
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))
        
    if request.method == 'POST':
        if User.query.filter_by(username=request.form.get('username')).first():
            flash('Username already exists', 'error')
            return render_template('auth/register.html')
            
        if User.query.filter_by(email=request.form.get('email')).first():
            flash('Email already registered', 'error')
            return render_template('auth/register.html')
            
        user = User(
            username=request.form.get('username'),
            email=request.form.get('email')
        )
        user.set_password(request.form.get('password'))
        user.generate_api_key()
        
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        return redirect(url_for('core.index'))
        
    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('core.index'))

@auth_bp.route('/api-key', methods=['POST'])
@login_required
@limiter.limit("3 per day")
def generate_api_key():
    current_user.generate_api_key()
    db.session.commit()
    return jsonify({'api_key': current_user.api_key})

@auth_bp.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html')

@auth_bp.route('/change-password', methods=['POST'])
@login_required
@limiter.limit("3 per hour")
def change_password():
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    
    if not current_user.check_password(current_password):
        flash('Current password is incorrect', 'error')
        return redirect(url_for('auth.profile'))
        
    current_user.set_password(new_password)
    db.session.commit()
    flash('Password updated successfully', 'success')
    return redirect(url_for('auth.profile'))
