
from database import db
from models.gender import Gender
from sqlalchemy.orm import relationship



class Volunteer(db.Model):
    # children = relationship("Gender")
    __tablename__ = 'Волонтеры'
    id = db.Column('ID_волонтера', db.Integer, primary_key=True, autoincrement=True)
    last_name = db.Column('Фамилия', db.String(20))
    first_name = db.Column('Имя', db.String(20))
    middle_name = db.Column('Отчество', db.String(20))
    phone = db.Column('Телефон', db.Integer)
    birth_date = db.Column('Дата_рождения', db.Date)
    gender_id = db.Column('Пол', db.Integer, db.ForeignKey('Пол.ID_пола'))
    gender = db.relationship('Gender', backref='volunteers')
    address = db.Column('Адрес', db.Text)
    email = db.Column('Email', db.Text)