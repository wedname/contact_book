from os import abort

from flask import session, redirect

from apps.users.controller import app, login_required, render_template, request, flash, current_user
from apps.contacts.model import *


class ContactsController:

    def __init__(self):

        @app.route('/contacts', methods=['GET', 'POST'])
        @login_required
        def contacts():
            if request.method == 'GET':
                # print(current_user.name)
                return render_template('contacts.html', user=current_user.name,
                                       contacts=Contacts.query.filter_by(users_id=current_user.get_id()))

        @app.route('/add_contact', methods=['GET', 'POST'])
        @login_required
        def add_contact():
            if request.method == 'GET':
                return render_template('add_contact.html')

            if request.method == 'POST':
                if request.form['name'] and request.form['phone']:
                    contact = Contacts(users_id=current_user.get_id(), **request.form)
                    db.session.add(contact)
                    db.session.commit()
                    return redirect('/contacts')
                else:
                    flash('Please fill "name" and "phone"!')

        @app.route('/delete_contact/<int:id>', methods=['POST'])
        @login_required
        def delete_contact(id: int):
            contact = Contacts.query.filter_by(id=id).first()
            # print(current_user)
            if current_user.get_id() == contact.users_id:
                db.session.delete(contact)
                db.session.commit()
                return redirect('/contacts')
            return abort()

        @app.route('/edit_contact/<int:id>', methods=['POST'])
        @login_required
        def edit_contact(id: int):

            contact = Contacts.query.filter_by(id=id).first()
            if request.method == 'GET':
                if current_user.get_id() == contact.users_id:
                    return render_template('edit_contact.html', contact=contact)
                return abort()

            if request.method == 'POST':
                contact(**request.form)
                db.session.commit()
                return redirect('/contacts')
