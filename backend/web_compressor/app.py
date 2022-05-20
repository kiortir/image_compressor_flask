import os
from werkzeug.utils import secure_filename
from werkzeug.routing import BaseConverter
import flask_admin
from flask import Flask, abort, redirect, render_template, request, url_for, jsonify
from flask_admin import helpers as admin_helpers
from flask_admin.contrib import sqla
from flask_security import (Security, SQLAlchemyUserDatastore, current_user,
                            login_required)
from flask_security.utils import encrypt_password
from flask_migrate import Migrate
try:
    from web_compressor.models import db, User, Role
except ModuleNotFoundError:
    from models import db, User, Role

# Create Flask application
app = Flask(__name__,
            static_url_path='/static/',
            static_folder='web/static',
            template_folder='web/templates')
app.config.from_pyfile('config.py')
db.init_app(app)
migrate = Migrate(app, db)

UPLOAD_FOLDER = os.path.join(
    os.getcwd(), 'backend', 'web_compressor', 'web', 'static', 'images')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[-1].lower() in ALLOWED_EXTENSIONS
# Define models
# roles_users = db.Table(
#     'roles_users',
#     db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
#     db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
# )


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


# Create customized model view class
class MyModelView(sqla.ModelView):
    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.has_role('superuser')
                )

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))

# Flask views


# @app.before_first_request
# def create_user():
#     with app.app_context():
#         user_role = Role(name='user')
#         super_user_role = Role(name='superuser')
#         db.session.add(user_role)
#         db.session.add(super_user_role)
#         db.session.commit()

#         test_user = user_datastore.create_user(
#             first_name='Admin',
#             email='admin',
#             password=encrypt_password('admin'),
#             roles=[user_role, super_user_role]
#         )
#         db.session.commit()


admin = flask_admin.Admin(
    app,
    'Пример',
    base_template='my_master.html',
    template_mode='bootstrap4',
)

admin.add_view(MyModelView(Role, db.session, category="Team"))
admin.add_view(MyModelView(User, db.session, category="Team"))


@app.context_processor
def inject_debug():
    return dict(debug=app.debug)


@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app.url_map.converters['regex'] = RegexConverter


@app.route('/<regex("project.*"):_>/')
@login_required
def main(_):
    return render_template('app/index.j2', current_user=current_user.email)


@app.route('/api', methods=['GET', 'POST'])
def api():
    id = request.form['project_id']
    project_id = id if id != 'null' else 1
    path_list = []
    for file in request.files.getlist("images[]"):
        print(file.__dict__)
        # secure_filename(file.filename)
        full_dir = [secure_filename(
            path_part) if path_part != '../' else '' for path_part in file.filename.split('/')]
        filename = full_dir[-1]
        add_dir = full_dir[:-1]
        if not allowed_file(filename):
            continue
        folder = os.path.join(
            app.config['UPLOAD_FOLDER'], str(project_id), *add_dir)
        if not os.path.isdir(folder):
            os.mkdir(folder)
        fullpath = os.path.join(folder, filename)
        file.save(fullpath)
        path_list.append({
            "url": f'/static/images/{project_id}/{"/".join(add_dir)}/{filename}',
            "name": filename
        })
    return jsonify(path_list)


if __name__ == '__main__':
    app.run(debug=True)
