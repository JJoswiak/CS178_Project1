from flask import Flask, render_template
import pymysql
import creds  # Don't forget to import creds.py

app = Flask(__name__)

def get_connection():
    return pymysql.connect(
        host=creds.host,
        user=creds.user,
        password=creds.password,
        database=creds.db,
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def index():
    connection = get_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT title, year FROM movies LIMIT 10;")
            movies = cursor.fetchall()
    return render_template('index.html', movies=movies)

if __name__ == '__main__':
    app.run(debug=True)