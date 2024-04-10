from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from functools import wraps
from sqlalchemy import or_
from database import db
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, SECRET_KEY
from models.volunteer import Volunteer
# Import other models

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    app.config['SECRET_KEY'] = SECRET_KEY
    bcrypt = Bcrypt(app)
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    class User(UserMixin, db.Model):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        username = db.Column(db.String(100), unique=True)
        password = db.Column(db.String(100))
        role = db.Column(db.String(20), default='user')

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if user and bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('table_list'))
            else:
                return 'Invalid username or password'
        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @app.route('/')
    @login_required
    def index():
        volunteers = Volunteer.query.all()
        return render_template('index.html', volunteers=volunteers)

    @app.route('/add', methods=['GET', 'POST'])
    @login_required
    def add_volunteer():
        if request.method == 'POST':
            last_name = request.form['last_name']
            first_name = request.form['first_name']
            middle_name = request.form['middle_name']
            phone = request.form['phone']
            birth_date = request.form['birth_date']
            gender_id = request.form['gender_id']
            address = request.form['address']
            email = request.form['email']

            new_volunteer = Volunteer(last_name=last_name, first_name=first_name, middle_name=middle_name,
                                      phone=phone, birth_date=birth_date, gender_id=gender_id,
                                      address=address, email=email)
            db.session.add(new_volunteer)
            db.session.commit()
            return redirect(url_for('index'))
        return render_template('add_volunteer.html')

    @app.route('/edit/<int:volunteer_id>', methods=['GET', 'POST'])
    @login_required
    def edit_volunteer(volunteer_id):
        volunteer = Volunteer.query.get(volunteer_id)
        if request.method == 'POST':
            volunteer.last_name = request.form['last_name']
            volunteer.first_name = request.form['first_name']
            volunteer.middle_name = request.form['middle_name']
            volunteer.phone = request.form['phone']
            volunteer.birth_date = request.form['birth_date']
            volunteer.gender_id = request.form['gender_id']
            volunteer.address = request.form['address']
            volunteer.email = request.form['email']
            db.session.commit()
            return redirect(url_for('index'))
        return render_template('edit_volunteer.html', volunteer=volunteer)

    @app.route('/table/<table_name>')
    @login_required
    def table_view(table_name):
        # Проверка доступа к таблице в зависимости от роли пользователя
        if table_name not in get_allowed_tables():
            return 'Access denied'

        table = db.metadata.tables[table_name]
        query = db.session.query(table)

        search = request.args.get('search')
        if search:
            # Логика поиска
            search_fields = get_search_fields(table_name)
            search_conditions = []
            for field in search_fields:
                search_conditions.append(getattr(table.c, field).ilike(f'%{search}%'))
            query = query.filter(or_(*search_conditions))

        filter_field = request.args.get('filter_field')
        filter_value = request.args.get('filter_value')
        if filter_field and filter_value:
            # Логика фильтрации
            query = query.filter(getattr(table.c, filter_field) == filter_value)

        results = query.all()
        return render_template('table_view.html', table_name=table_name, results=results, table=table)

    def get_search_fields(table_name):
        if table_name == 'Волонтеры':
            return ['Фамилия', 'Имя', 'Отчество']
        elif table_name == 'Мероприятия':
            return ['Название']
        elif table_name == 'Проекты':
            return ['Название']
        # И так далее для остальных таблиц
        else:
            return []
    def get_allowed_tables():
        if current_user.role == 'boss':
            return ['Волонтеры', 'Мероприятия', 'Проекты', 'Должности', 'Личное_дело',
                    'Медицинская_карта', 'Паспорта', 'Удостоверения', 'Изменения_должностей',
                    'Изменения_статусов', 'Участники_мероприятий', 'Участники_проектов']
        elif current_user.role == 'secretary':
            return ['Волонтеры', 'Личное_дело', 'Паспорта', 'Удостоверения']
        elif current_user.role == 'coordinator':
            return ['Волонтеры', 'Мероприятия', 'Проекты', 'Участники_мероприятий', 'Участники_проектов']
        else:
            return []

    @app.route('/table_list')
    @login_required
    def table_list():
        tables = get_allowed_tables()
        return render_template('table_list.html', tables=tables)

    return app


app = create_app()

if __name__ == '__main__':
    app.run()