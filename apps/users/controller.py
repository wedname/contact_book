from flask import render_template, request, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user

from config import app
from apps.users.model import *


class UsersController:

    def __init__(self):

        @app.route('/login', methods=['GET', 'POST'])
        def login():
            if request.method == 'GET':
                if current_user.is_authenticated:
                    return redirect('/contacts')
                return render_template('login.html')

            if request.method == 'POST':
                email = request.form.get('email')
                password = request.form.get('password')

                if login and password:
                    user = Users.query.filter_by(email=email).first()

                    if user and check_password_hash(user.password_hash, password):
                        login_user(user)
                        return redirect('/contacts')
                    else:
                        flash('Login or password incorrect')
                else:
                    flash('Please fill login and password fields.')
                return render_template('login.html')

        @app.route('/register', methods=['GET', 'POST'])
        def register():
            name = request.form.get('name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')

            if request.method == 'POST':
                if not (name or login or phone or password or confirm_password):
                    flash('Please, fill all fields!')
                elif password != confirm_password:
                    flash('Passwords are not equal!')
                else:
                    hash_password = generate_password_hash(password)
                    new_user = Users(name=name, email=email, phone=phone, password_hash=hash_password)
                    db.session.add(new_user)
                    db.session.commit()
                    return redirect('/login')
            return render_template('register.html')

        @app.route('/logout', methods=['GET', 'POST'])
        @login_required
        def logout():
            logout_user()
            return redirect('/login')

        @app.after_request
        def redirect_to_login(response):
            if response.status_code == 401:
                return redirect('/login' + '?next=' + request.url)
            return response
