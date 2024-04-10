from database import db

class Volunteer(db.Model):
    __tablename__ = 'Волонтеры'
    id = db.Column('ID_волонтера', db.Integer, primary_key=True)
    last_name = db.Column('Фамилия', db.String(20))
    first_name = db.Column('Имя', db.String(20))
    middle_name = db.Column('Отчество', db.String(20))
    phone = db.Column('Телефон', db.Integer)
    birth_date = db.Column('Дата_рождения', db.Date)
    gender_id = db.Column('Пол', db.Integer, db.ForeignKey('Пол.ID_пола'))
    address = db.Column('Адрес', db.Text)
    email = db.Column('Email', db.Text)
    photo = db.Column('Фото', db.LargeBinary)