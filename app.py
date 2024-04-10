from flask import Flask, render_template, request, redirect, url_for
from database import db
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
from models.volunteer import Volunteer
# Import other models

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    db.init_app(app)

    @app.route('/')
    def index():
        volunteers = Volunteer.query.all()
        return render_template('index.html', volunteers=volunteers)

    @app.route('/add', methods=['GET', 'POST'])
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
            # Обработка загрузки фото
            photo = request.files['photo'].read() if 'photo' in request.files else None

            new_volunteer = Volunteer(last_name=last_name, first_name=first_name, middle_name=middle_name,
                                      phone=phone, birth_date=birth_date, gender_id=gender_id,
                                      address=address, email=email, photo=photo)
            db.session.add(new_volunteer)
            db.session.commit()
            return redirect(url_for('index'))
        return render_template('add_volunteer.html')

    @app.route('/edit/<int:volunteer_id>', methods=['GET', 'POST'])
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
            if 'photo' in request.files:
                volunteer.photo = request.files['photo'].read()
            db.session.commit()
            return redirect(url_for('index'))
        return render_template('edit_volunteer.html', volunteer=volunteer)

    return app


app = create_app()

if __name__ == '__main__':
    app.run()