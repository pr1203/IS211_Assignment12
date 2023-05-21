from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import g
import sqlite3 as lite

database = 'hw13.db'
username = 'admin'
password = 'password'

app = Flask(__name__)
app.config['DATABASE'] = database
app.secret_key = 'dev'

def init_db():
    db = get_db()
    with app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def connect_db():
    db = lite.connect(database)
    db.row_factory = lite.Row
    return db


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = lite.connect(database)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.before_request
def before_request():
    g.db = connect_db()


@app.route('/')
def index():
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'password':
                return redirect('/dashboard')
        else:
            print("Invalid username or password")
            return render_template('login.html')

    else:
        return render_template('login.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if session['username'] == 'admin':
        cur = g.db.execute('SELECT student_id, first_name, last_name FROM Students order by student_id')
        students = [dict(student_id=row[0], first_name=row[1], last_name=row[2]) for row in cur.fetchall()]
        cur2 = g.db.execute('SELECT quiz_id, subject, number_of_questions, quiz_date FROM Quizzes order by quiz_id')
        quizzes = [dict(quiz_id=row[0], subject=row[1], number_of_questions=row[2], quiz_date=row[3]) for row in cur2.fetchall()]

        return render_template('dashboard.html', students=students, quizzes=quizzes)
    else:
        return redirect('/login')

@app.route('/student/add', methods=['GET', 'POST'])
def add_student():
    if session['username'] == 'admin':
        if request.method == 'GET':
            return render_template('add_student.html')
        elif request.method == 'POST':
            try:
                g.db.execute("INSERT INTO Students (first_name, last_name) VALUES (?, ?)", (request.form['first_name'], request.form['last_name']))
                g.db.commit()
                return redirect('/dashboard')
            except Exception as e:
                print(e)
                return render_template('add_student.html')
    else:
        return redirect('/login')

@app.route('/quiz/add', methods=['GET', 'POST'])
def add_quiz():
    if session['username'] == 'admin':
            if request.method == 'GET':
                return render_template('add_quiz.html')
            elif request.method == 'POST':
                try:
                    g.db.execute("INSERT INTO quizzes (subject, number_of_questions, quiz_date) VALUES (?, ?, ?)", [request.form['subject'], request.form['number_of_questions'], request.form['quiz_date']])
                    g.db.commit()
                    return redirect('/dashboard')
                except Exception as e:
                    print(e)
                    return render_template('add_quiz.html')
    else:
        return redirect('/login')

@app.route('/student/<id>')
def view_results(id):
    if session['username'] == 'admin':
        cur = g.db.execute(
            'SELECT Quizzes.quiz_id, Quizzes.subject, Quizzes.quiz_date, Quiz_Results.result '
            'FROM Quiz_Results INNER JOIN Quizzes ON Quiz_Results.quiz_id = Quizzes.quiz_id '
            'INNER JOIN Students ON Quiz_Results.student_id = Students.student_id '
            'WHERE Students.student_id = ?',
            [id]
        )

        res = cur.fetchall()
        student_results = [dict(quiz_id=row[0], subject=row[1], quiz_date=row[2], result=row[3]) for row in res]
        return render_template('view_student_results.html', student_results=student_results)
    else:
        return redirect('/login')

@app.route('/results/add', methods=['GET', 'POST'])
def add_result():
    if session['username'] == 'admin':
        try:
            if request.method == 'GET':
                cur = g.db.execute("SELECT student_id, first_name, last_name FROM students ORDER BY student_id")
                students = [dict(student_id=row[0], first_name=row[1], last_name=row[2]) for row in cur.fetchall()]
                cur2 = g.db.execute("SELECT quiz_id, subject FROM quizzes ORDER BY quiz_id")
                quizzes = [dict(quiz_id=row[0], subject=row[1]) for row in cur2.fetchall()]
                return render_template('add_quiz_results.html', students=students, quizzes=quizzes)

            elif request.method == 'POST':
                g.db.execute("INSERT INTO results (student_id, quiz_id, result) VALUES (?, ?, ?)", [request.form['add_student'], request.form['add_quiz'], request.form['add_result']])
                g.db.commit()
                return redirect('/dashboard')
        except Exception as e:
            print(e)
            return redirect('/results/add')

if __name__ == "__main__":
    app.run(debug=True)
    connect_db()

    
