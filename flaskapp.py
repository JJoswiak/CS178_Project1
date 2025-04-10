from flask import Flask, render_template, request, redirect, url_for, flash
import sql_connect

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for using flash messages

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add-movie', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        # Extract form data
        title = request.form['title']
        genre = request.form['genre']
        
        # Insert movie into the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO movies (title, genre) VALUES (%s, %s)', (title, genre))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Movie added successfully!', 'success')  # Display success message
        return redirect(url_for('home'))
    else:
        return render_template('add_movie.html')

@app.route('/delete-movie', methods=['GET', 'POST'])
def delete_movie():
    if request.method == 'POST':
        title = request.form['title']

        # Delete movie from the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM movies WHERE title = %s', (title,))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Movie deleted successfully!', 'success')  # Display success message
        return redirect(url_for('home'))
    else:
        return render_template('delete_movie.html')

@app.route('/display-movies')
def display_movies():
    # Fetch movies from the database
    conn = sql_connect.get_conn()
    cursor = conn.cursor()
    cursor.execute('SELECT title, genre FROM movies')
    movies = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('display_movies.html', movies=movies)


# These two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)