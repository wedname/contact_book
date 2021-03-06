from flask import redirect
from werkzeug.exceptions import abort

from apps.users.controller import app, login_required, render_template, request, flash, current_user
from apps.contacts.model import *


class ContactsController:

    def __init__(self):

        @app.route('/contacts', methods=['GET', 'POST'])
        @login_required
        def contacts():
            if request.method == 'GET':
                all_users_contacts = Contacts.query.order_by(Contacts.name.asc()).filter_by(
                    users_id=current_user.get_id())
                groups = Contacts.query.order_by(Contacts.group.asc()).filter_by(
                    users_id=current_user.get_id())

                return render_template('contacts.html', user=current_user.name, contacts=all_users_contacts,
                                       groups=groups)

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

        @app.route('/delete_contact/<int:id>')
        @login_required
        def delete_contact(id: int):
            contact = Contacts.query.filter_by(id=id).first()
            if int(current_user.get_id()) == contact.users_id:
                db.session.delete(contact)
                db.session.commit()
                return redirect('/contacts')
            return abort(404)

        @app.route('/edit_contact/<int:id>', methods=['GET', 'POST'])
        @login_required
        def edit_contact(id: int):
            contact = Contacts.query.filter_by(id=id).first()
            if request.method == 'GET':
                if int(current_user.get_id()) == contact.users_id:
                    return render_template('edit_contact.html', contact=contact)
                return abort(404)

            if request.method == 'POST':
                contact(**request.form)
                db.session.commit()
                return redirect('/contacts')

        @app.route('/search_contacts/')
        @login_required
        def search_contacts():
            groups = Contacts.query.order_by(Contacts.group.asc()).filter_by(
                users_id=current_user.get_id())
            query = request.args.get('query')
            search = "%{}%".format(query)
            result = Contacts.query.filter(Contacts.name.like(search)).filter_by(users_id=current_user.get_id()).all()
            return render_template('contacts.html', user=current_user.name, contacts=result, groups=groups)

        @app.route('/contacts/sort_by_name/<name>')
        @login_required
        def sort_by_name(name):
            groups = Contacts.query.order_by(Contacts.group.asc()).filter_by(
                users_id=current_user.get_id())
            if name == 'asc':
                result = Contacts.query.order_by(Contacts.name.asc()).filter_by(users_id=current_user.get_id()).all()
                return render_template('contacts.html', user=current_user.name, contacts=result, groups=groups)
            elif name == 'desc':
                result = Contacts.query.order_by(Contacts.name.desc()).filter_by(users_id=current_user.get_id()).all()
                return render_template('contacts.html', user=current_user.name, contacts=result, groups=groups)

        @app.route('/contacts/<group>')
        @login_required
        def sort_by_group(group: str):
            groups = Contacts.query.order_by(Contacts.group.asc()).filter_by(
                users_id=current_user.get_id())
            if group == 'all':
                all_users_contacts = Contacts.query.order_by(Contacts.name.asc()).filter_by(
                    users_id=current_user.get_id())
                return render_template('contacts.html', user=current_user.name, contacts=all_users_contacts,
                                       groups=groups)

            result = Contacts.query.order_by(Contacts.name.asc()).filter_by(group=group,
                                                                            users_id=current_user.get_id()).all()
            return render_template('contacts.html', user=current_user.name, contacts=result, groups=groups)

        # TODO:
        #  ?????????????????????? ???????????????????? ????????
        #  ?????????????????????? contacts/controller ?? user/controller
        #  ?????????????? ?????????? ?? ?????????????????? ????????
        #  ???????????? ???????????? ??????????????
