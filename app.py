from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

app = Flask(__name__)

db = mysql.connector.connect(
  host=DB_HOST,
  user=DB_USER,
  password=DB_PASSWORD,
  database=DB_NAME
)


@app.route('/')
def volunteers():
    cursor = db.cursor()
    query = "SELECT * FROM Волонтеры"
    cursor.execute(query)
    volunteers = cursor.fetchall()
    cursor.close()
    return render_template('volunteers.html', volunteers=volunteers)


if __name__ == '__main__':
    app.run()
