from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)

# Configure your MySQL connection
# Replace the values with your database credentials
# Ensure you have the appropriate MySQL driver installed for Python
import mysql.connector
app.secret_key = '12345678'
try:
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Kaalan@123',
        database='PROJECT'
        
    )

    # Create a cursor to interact with the database
    cursor = db.cursor()
except mysql.connector.Error as err:
    print(f"Error connecting to MySQL: {err}")

@app.route('/')
def login_page():
    return render_template('login.html')  # Replace 'your_html_file_name' with the actual file name

@app.route('/login', methods=['POST'])

def login():
    print("Inside login route") 
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Query to fetch user data from the database based on username and password
        query = "SELECT * FROM Users WHERE Username = %s AND Password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        print(f"User found: {user}")

        if user:
            session['username'] = username
            # Authentication successful, redirect to main_page with the username
            return redirect(url_for('home', username=username))

        # If authentication fails, redirect back to login page or handle accordingly
        return redirect(url_for('login'))
    return render_template('login.html', error='Login failed. Please check your username and password.')


@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return redirect(url_for('table'))
    # Assuming you want to display faculty data on the home page
    query = "SELECT * FROM faculty"
    cursor.execute(query)
    data = cursor.fetchall()

    # Modify the data to split each cell content into words
    modified_data = []
    for row in data:
        modified_row = []
        for cell_content in row:
            # Split the content into words
            words = cell_content.split()
            modified_row.append(words)
        modified_data.append(modified_row)
    return render_template('home.html', faculty=modified_data)

@app.route('/table')
def table():
    semester = request.args.get('semester', 'S5')  # Default to S5 if not specified

    # Modify the data to split each cell content into words
    query = f"SELECT * FROM timetable_{semester}"
    cursor.execute(query)
    data = cursor.fetchall()

    modified_data = []
    for row in data:
        modified_row = []
        for cell_content in row:
            words = cell_content.split()
            modified_row.append(words)
        modified_data.append(modified_row)

    return render_template('table.html', timetable=modified_data, semester=semester)

@app.route('/show_timetable', methods=['POST'])
def show_timetable():
    if request.method == 'POST':
        semester = request.form.get('semester', 'S5')  # Default to S5 if not specified

        # Assuming you want to display timetable data on the table page
        query = f"SELECT * FROM timetable_{semester}"
        cursor.execute(query)
        data = cursor.fetchall()

        # Modify the data to split each cell content into words
        modified_data = []
        for row in data:
            modified_row = []
            for cell_content in row:
                # Split the content into words
                words = cell_content.split()
                modified_row.append(words)
            modified_data.append(modified_row)

        return render_template('table.html', timetable=modified_data, semester=semester)

    return redirect(url_for('home'))

@app.route('/home')
def home_page():
    # Assuming you want to display faculty data on the home page
    query = "SELECT * FROM faculty"
    cursor.execute(query)
    data = cursor.fetchall()

    # Modify the data to split each cell content into words
    modified_data = []
    for row in data:
        modified_row = []
        for cell_content in row:
            # Split the content into words
            words = cell_content.split()
            modified_row.append(words)
        modified_data.append(modified_row)
    return render_template('home.html', faculty=modified_data)


@app.route('/submit', methods=['POST'])
def submit():
    id = request.form.get('facultyId')
    name = request.form.get('facultyName')
    course = request.form.get('facultyCourse')
    classs = request.form.get('facultyClass')
    
    cursor.execute(f"INSERT INTO FACULTY VALUES ('{id}','{name}','{course}','{classs}')")
    db.commit()
    return redirect(url_for('home'))

@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    print(id)
    
    cursor.execute(f"DELETE FROM FACULTY WHERE FACID={str(id)}")
    db.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

