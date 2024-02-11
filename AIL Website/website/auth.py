from flask import Blueprint, render_template, request, redirect, url_for, session
from website.models import mydb, mycursor
from spellchecker import SpellChecker
from flask import flash
from collections import Counter
from flask import jsonify, json

auth = Blueprint('auth', __name__)


spell = SpellChecker()

@auth.route('/')
def default():
    return render_template("login.html", boolean=True)

def check_credentials(username, password):
    
    if username.isdigit() and 1000 <= int(username) <= 1999:
        mycursor.execute("SELECT st_pass FROM student WHERE st_id = %s", (username,))
        result = mycursor.fetchone()

        if result and result[0] == password:
            return True, "student"  # Authentication successful, role is "student"

    elif username.isdigit() and 3000 <= int(username) <= 3999:
        mycursor.execute("SELECT admin_pass FROM admin WHERE admin_id = %s", (username,))
        result = mycursor.fetchone()

        if result and result[0] == password:
            return True, "admin"  # Authentication successful, role is "admin"

    return False, None  # Authentication failed



# Login route
@auth.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        auth_result, role = check_credentials(username, password)

        if auth_result:
            # Store the username and role in the session
            session['username'] = username
            session['role'] = role

            if role == "student":
                # Retrieve additional information for the student
                student_info = get_student_info(username)
                grades_info = get_grades(username)
                user_name = get_student_name(session['username'])
                flash('Login successful', 'success')

                return render_template("home.html", student_info=student_info, grades_info=grades_info,user_name=user_name)
            elif role == "admin":
                admin_info = get_admin_info(username)
                user_name = get_admin_name(session['username'])
                return render_template("admin_home.html",admin_info=admin_info, user_name=user_name)
        else:
            return render_template("login.html", boolean=True)

    return redirect(url_for('auth.default'))

def get_student_info(username):
    query = """
        SELECT st_name, st_email, st_picture_path, penalized
        FROM student
        WHERE st_id = %s
    """

    # Execute the query with the username parameter
    mycursor.execute(query, (username,))
    
    result = mycursor.fetchone()

    # Return the result as a dictionary
    student_info = {
        'name': result[0],
        'email': result[1],
        'picture': result[2],
        'penalized': bool(result[3])  
    }


    return student_info

@auth.route('/logout')
def logout():
    # Clear the session to log out the user
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('auth.default'))


@auth.route('/home')  
def home():
    if 'username' in session and session['role'] == 'student':
        # Fetch the student's info from the database
        user_name = get_student_name(session['username'])
        student_info = get_student_info(session['username'])
        grades_info = get_grades(session['username'])
        return render_template("home.html", user_name=user_name, student_info=student_info,grades_info=grades_info)
    else:
        return redirect(url_for('auth.default'))
    
@auth.route('/admin_home')  
def admin_home():
    if 'username' in session and session['role'] == 'admin':
        # Fetch the admin's name from the database
        user_name = get_admin_name(session['username'])
        admin_info = get_admin_info(session['username'])

        return render_template("admin_home.html", user_name=user_name,admin_info=admin_info)
    else:
        return redirect(url_for('auth.default'))

def get_admin_name(admin_id):
    mycursor.execute("SELECT admin_name FROM admin WHERE admin_id = %s", (admin_id,))
    result = mycursor.fetchone()
    return result[0] if result else None

def get_student_name(student_id):
    mycursor.execute("SELECT st_name FROM student WHERE st_id = %s", (student_id,))
    result = mycursor.fetchone()
    if result:
        return result[0]
    else:
        return "Unknown"
    
from spellchecker import SpellChecker

@auth.route('/search', methods=['GET', 'POST'])
def search():
    if 'username' in session:
        role = session.get('role')

        if role == 'student':
            # Fetch the student's name from the database
            user_name = get_student_name(session['username'])
        elif role == 'admin':
            # Fetch the admin's name from the database
            user_name = get_admin_name(session['username'])
        else:
            # Handle other roles or unauthorized access
            return redirect(url_for('auth.default'))

        spell = SpellChecker()

        if request.method == 'POST':
            # Handle form submission
            book_search = request.form.get('book_search', '')

            # Perform spell checking on the search term
            misspelled = spell.unknown([book_search])

            # If there are misspelled words, suggest corrections
            if misspelled:
                suggestions = spell.candidates(list(misspelled)[0])
            else:
                suggestions = []

            # Perform a query in your database using book_search
            query = """
                SELECT book_title, book_author, genre, specialty, book_picture_path, location FROM book
                WHERE LOWER(book_title) LIKE LOWER(%s)
                   OR LOWER(book_author) LIKE LOWER(%s)
                   OR LOWER(genre) LIKE LOWER(%s)
                   OR LOWER(specialty) LIKE LOWER(%s)
            """
            mycursor.execute(query, ('%' + book_search + '%', '%' + book_search + '%', '%' + book_search + '%', '%' + book_search + '%'))
            search_results = mycursor.fetchall()

            return render_template("bookSearch.html", user_name=user_name, ss=search_results, suggestions=suggestions)

        # Fetch book names, authors, and genres from the database
        book_names = get_book_names()
        authors = get_book_authors()
        genres = get_book_genre()

        return render_template("search.html", user_name=user_name, book_names=book_names, authors=authors, genres=genres)

    return redirect(url_for('auth.default'))






def get_book_names():
    query = """
        SELECT book_title FROM book
    """

    mycursor.execute(query)
    
    result = mycursor.fetchall()

    # Extract book names from the result and return as a list
    book_names = [row[0] for row in result]
    
    return book_names

def get_book_authors():
    query = """
        SELECT DISTINCT book_author FROM book
    """

    mycursor.execute(query)
    
    result = mycursor.fetchall()

    # Extract book names from the result and return as a list
    book_authors = [row[0] for row in result]
    
    return book_authors

def get_book_genre():
    query = """
        SELECT DISTINCT genre FROM book
    """

    mycursor.execute(query)
    
    result = mycursor.fetchall()

    # Extract book names from the result and return as a list
    book_genre = [row[0] for row in result]
    
    return book_genre

def get_grades(username):
    query = """
        SELECT c.course_name, g.grade
        FROM grades g
        JOIN course c ON g.course_id = c.course_id
        WHERE g.st_id = (
            SELECT st_id
            FROM student
            WHERE st_id= %s
        )
    """

    # Execute the query with the username parameter
    mycursor.execute(query, (username,))

    # Fetch all the results
    results = mycursor.fetchall()

    # Return a list of dictionaries containing course_name and grade
    grades_info = [{'course_name': result[0], 'grade': result[1]} for result in results]

    return grades_info


def get_admin_info(username):
    query = """
        SELECT admin_name, admin_email, admin_picture_path, phone_number
        FROM admin
        WHERE admin_id = %s
    """

    # Execute the query with the username parameter
    mycursor.execute(query, (username,))
    
    result = mycursor.fetchone()

    # Return the result as a dictionary
    admin_info = {
        'name': result[0],
        'email': result[1],
        'picture': result[2],
        'number': result[3]  
    }
    return admin_info

@auth.route('/manage')
def manage():
    if 'username' in session and session['role'] == 'admin':
         user_name = get_admin_name(session['username'])
         return render_template('manage.html',user_name=user_name)


@auth.route('/add')
def add():
    if 'username' in session and session['role'] == 'admin':
         user_name = get_admin_name(session['username'])
         book_names = get_book_names()
         return render_template('add.html',user_name=user_name, book_names=book_names)

@auth.route('/update')
def update():
    if 'username' in session and session['role'] == 'admin':
         user_name = get_admin_name(session['username'])
         return render_template('update.html',user_name=user_name)
    

@auth.route('/remove')
def remove():
    if 'username' in session and session['role'] == 'admin':
         user_name = get_admin_name(session['username'])
         return render_template('remove.html',user_name=user_name)
    
@auth.route('/bookSearch')
def bookSearch():
    if 'username' in session:
        role = session.get('role')

        if role == 'student':
            # Fetch the student's name from the database
            user_name = get_student_name(session['username'])
        elif role == 'admin':
            # Fetch the admin's name from the database
            user_name = get_admin_name(session['username'])
        else:
            # Handle other roles or unauthorized access
            return redirect(url_for('auth.default'))


    return render_template("bookSearch.html", user_name=user_name)



def get_all_books():
    query = """
        SELECT book_id, book_title, book_author, genre, available, specialty, difficulty, book_picture_path, location FROM book
    """
    mycursor.execute(query)
    result = mycursor.fetchall()

    # Extract book information from the result and return as a list of dictionaries
    books_info = [
        {
            "book_id": row[0],
            "book_title": row[1],
            "book_author": row[2],
            "genre": row[3],
            "available": row[4],
            "specialty": row[5],
            "difficulty": row[6],
            "book_picture_path": row[7],
            "location": row[8],
        }
        for row in result
    ]
    return books_info

def check_book_id_exists(book_id):
    query = "SELECT * FROM book WHERE book_id = %s"
    params = (book_id,)

    # Execute the query
    mycursor.execute(query, params)
    
    # Fetch the result
    result = mycursor.fetchone()

    # Check if the result is not None (book exists)
    return result is not None

def update_book_attribute(book_id, attribute, new_value):
    # Check if the book ID exists
    if not check_book_id_exists(book_id):
        return False  # Book ID does not exist, return False

    # Define the query to update the attribute
    query = f"UPDATE book SET {attribute} = %s WHERE book_id = %s"
    params = (new_value, book_id)

    # Execute the update query using your existing cursor
    mycursor.execute(query, params)

    # Commit the changes to the database using your existing connection
    mydb.commit()

    return True  # Update successful

@auth.route('/update_book', methods=['POST'])
def update_book():
    if 'username' in session and session['role'] == 'admin':
         user_name = get_admin_name(session['username'])
    if request.method == 'POST':
        book_id = request.form['book_id']
        attribute = request.form['attribute']
        new_value = request.form['new_value']

        # Check if the book ID exists
        if not check_book_id_exists(book_id):
            return render_template("update.html", book_id_exists=False)

        # Update the book attribute
        success = update_book_attribute(book_id, attribute, new_value)

        if success:
            return render_template("update.html", book_id_exists=True, update_success=True,user_name=user_name)
        else:
            return render_template("update.html", book_id_exists=True, update_success=False,user_name=user_name)

    return redirect(url_for('auth.default'))

@auth.route('/add_book', methods=['POST'])
def add_book():
    if 'username' in session and session['role'] == 'admin':
         user_name = get_admin_name(session['username'])
    if request.method == 'POST':
        # Retrieve form data
        book_id = request.form.get('book_id')
        book_title = request.form.get('book_title')
        author = request.form.get('author')
        genre = request.form.get('genre')
        no_of_copies = request.form.get('no_of_copies')
        specialty = request.form.get('specialty')
        difficulty = request.form.get('difficulty')
        picture_path = request.form.get('picture')

        # Perform database insertion
        query = """
            INSERT INTO book (book_id, book_title, book_author, genre, available, specialty, difficulty, book_picture_path)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (book_id, book_title, author, genre, no_of_copies, specialty, difficulty, picture_path)

        try:
            mycursor.execute(query, values)
            mydb.commit()
            return render_template("add.html", success=True,user_name=user_name)
        except Exception as e:
            print("Error:", e)
            mydb.rollback()
            return render_template("add.html", success=False,user_name=user_name)

    return redirect(url_for('login'))

@auth.route('/remove_book', methods=['POST'])
def remove_book():
    if 'username' in session and session['role'] == 'admin':
         user_name = get_admin_name(session['username'])
    if request.method == 'POST':
        # Retrieve book ID from the form
        book_id = request.form.get('book_id')

        # Perform database deletion
        query = """
            DELETE FROM book
            WHERE book_id = %s
        """
        values = (book_id,)

        try:
            mycursor.execute(query, values)
            mydb.commit()
            return render_template("remove.html", success=True,user_name=user_name)
        except Exception as e:
            print("Error:", e)
            mydb.rollback()
            return render_template("remove.html", success=False,user_name=user_name)

    return redirect(url_for('login'))


@auth.route('/stats')
def stats():
    if 'username' in session:
        role = session.get('role')

        if role == 'student':
            # Fetch the student's name from the database
            user_name = get_student_name(session['username'])
        elif role == 'admin':
            # Fetch the admin's name from the database
            user_name = get_admin_name(session['username'])
        else:
            # Handle other roles or unauthorized access
            return redirect(url_for('auth.default'))

        # Query to get book search history
        search_history_query = """
            SELECT book_id FROM history
        """
        mycursor.execute(search_history_query)
        search_history = [result[0] for result in mycursor.fetchall()]

        # Count occurrences of each book_id in search history
        search_counts = Counter(search_history)

        # Query to get book read history
        read_history_query = """
            SELECT book_id FROM preference
        """
        mycursor.execute(read_history_query)
        read_history = [result[0] for result in mycursor.fetchall()]

        # Count occurrences of each book_id in read history
        read_counts = Counter(read_history)

        # Prepare data for charts
        search_labels = list(search_counts.keys())
        search_values = list(search_counts.values())
        read_labels = list(read_counts.keys())
        read_values = list(read_counts.values())

        return render_template(
            "stats.html",
            user_name=user_name,
            search_labels_json=json.dumps(search_labels),
            search_values_json=json.dumps(search_values),
            read_labels_json=json.dumps(read_labels),
            read_values_json=json.dumps(read_values)
        )

    return redirect(url_for('auth.default'))


@auth.route('/contact')
def contact():
    if 'username' in session and session['role'] == 'student':
        user_name = get_student_name(session['username'])
        

        return render_template("contact.html", user_name=user_name, allAdmin = get_all_admin())
    

def get_all_admin():
    query = """
        SELECT admin_name, admin_email, admin_picture_path, phone_number
        FROM admin
    """

    # Execute the query with the username parameter
    mycursor.execute(query)

    # Fetch all the results
    results = mycursor.fetchall()

    # Define a list to store dictionaries
    admin_list = []

    # Iterate over the results and create dictionaries
    for row in results:
        admin_data = {
            'admin_name': row[0],
            'admin_email': row[1],
            'admin_picture_path': row[2],
            'phone_number': row[3],
        }
        admin_list.append(admin_data)

    # Return the list of dictionaries
    return admin_list


@auth.route('/view')
def view():
    if 'username' in session and session['role'] == 'student':
        user_name = get_student_name(session['username'])
        

        return render_template("view.html", user_name=user_name, allBooks = get_all_books())
    

@auth.route('/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('query', '')

    # Perform a query in your database to get autocomplete suggestions
    autocomplete_query = """
        SELECT DISTINCT book_title
        FROM book
        WHERE book_title COLLATE utf8mb4_general_ci LIKE %s
    """
    mycursor.execute(autocomplete_query, ('%' + query + '%',))
    suggestions = [result[0] for result in mycursor.fetchall()]

    return jsonify(suggestions)

@auth.route('/suggestion')
def suggestion():
    if 'username' in session and session['role'] == 'student':
        student_id = session['username']
        username = get_student_name(session['username'])

        return render_template("suggestion.html", suggestedBook=get_book_suggestions(student_id), username=username)
    
import pickle
import pandas as pd
from sklearn.preprocessing import LabelEncoder


with open('knn_model.pkl', 'rb') as file:
    loaded_knn_model = pickle.load(file)

def get_suggestions(student_id):
    query = """
        SELECT grades.course_id, grades.grade, course.specialty, course.difficulty, grades.pass
        FROM grades
        JOIN course ON grades.course_id = course.course_id
        WHERE grades.st_id = %s;
        """
    mycursor.execute(query, (student_id,))

    results = mycursor.fetchall()


    suggestion_list = []

    for row in results:
        suggestion_data = {
            'course_id': row[0],
            'grade': row[1],
            'specialty': row[2],
            'difficulty': row[3],
            'pass': row[4]
        }
        
        suggestion_list.append(suggestion_data)

    # Create a new Label Encoder and encode 'specialty' for this function
    label_encoder_function = LabelEncoder()
    for suggestion_data in suggestion_list:
        suggestion_data['specialty'] = label_encoder_function.fit_transform([suggestion_data['specialty']])[0]

    # Use the loaded KNN model for predictions
    for suggestion_data in suggestion_list:
        input_data = [[
            suggestion_data['course_id'],
            suggestion_data['grade'],
            suggestion_data['specialty'],
            suggestion_data['difficulty'],
            suggestion_data['pass']
        ]]
        
        predictions_list = []
    for suggestion_data in suggestion_list:
        input_data = pd.DataFrame([suggestion_data]) 
        prediction = loaded_knn_model.predict(input_data)
        predictions_list.append(prediction)

    return predictions_list

def get_book_suggestions(student_id):
    query = """select * from book
            where book_id = %s"""
    suggestion_list = []

    book_ids = get_suggestions(student_id)

    for book_id in book_ids:
        mycursor.execute(query, (int(book_id[0]),))  
        results = mycursor.fetchall()
        for book in results:
            books_info ={
                "book_id": book[0],
                "book_title": book[1],
                "book_author": book[2],
                "genre": book[3],
                "available": book[4],
                "specialty": book[5],
                "difficulty": book[6],
                "book_picture_path": book[7],
                "location": book[8],
            }
            suggestion_list.append(books_info)
            
    return suggestion_list

        
