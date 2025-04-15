from flask import Flask, render_template, request, redirect, url_for, flash
import sql_connect
from dynamo_code import add_user, get_all_users
from dynamo_code import update_user_genre, delete_user


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
        cursor.execute('INSERT INTO movie (title, genre) VALUES (%s, %s)', (title, genre))
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
        cursor.execute('DELETE FROM movie WHERE title = %s', (title,))
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
    cursor.execute('SELECT title FROM movie')
    movies = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('display_movies.html', movies=movies)

@app.route('/add-user', methods=['GET', 'POST'])
def add_user_route():
    if request.method == 'POST':
        first = request.form['first_name']
        last = request.form['last_name']
        genre = request.form['favorite_genre']
        
        add_user(first, last, genre)
        flash('User added successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('add_user.html')

@app.route('/display-users')
def display_users():
    users = get_all_users()
    user_list = [(u['FirstName'], u['LastName'], u['FavoriteGenre']) for u in users]
    return render_template('display_users.html', users=user_list)

@app.route('/update-user', methods=['GET', 'POST'])
def update_user_route():
    if request.method == 'POST':
        first = request.form['first_name']
        last = request.form['last_name']
        new_genre = request.form['new_genre']
        
        update_user_genre(first, last, new_genre)
        flash('User updated successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('update_user.html')

@app.route('/delete-user', methods=['GET', 'POST'])
def delete_user_route():
    if request.method == 'POST':
        first = request.form['first_name']
        last = request.form['last_name']
        
        delete_user(first, last)
        flash('User deleted successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('delete_user.html')

# These two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)