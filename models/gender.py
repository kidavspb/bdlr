from database import db



class Gender(db.Model):
    __tablename__ = 'Пол'
    id = db.Column('ID_пола', db.Integer, primary_key=True)
    name = db.Column('Название', db.String(20))