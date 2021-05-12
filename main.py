from apps.users.controller import *
from apps.contacts.controller import *


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(Users).get(user_id)


@app.route('/')
def main_page():
    return render_template('index.html')


if __name__ == '__main__':
    users = UsersController()
    contacts = ContactsController()
    app.run(host='localhost', port=5000)
