from flask import Flask
from database import db
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
from models.volunteer import Volunteer
# Import other models

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

    db.init_app(app)

    return app

app = create_app()

if __name__ == '__main__':
    app.run()