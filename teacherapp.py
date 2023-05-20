from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hw13.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(200), nullable=False)
    lastname = db.Column(db.String(200), nullable=False)

    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname


class Quizzes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    qcount = db.Column(db.Integer, nullable=False)
    dategiven = db.Column(db.Integer, nullable=False)

    def __init__(self, subject, qcount, dategiven):
        self.subject = subject
        self.qcount = qcount
        self.dategiven = dategiven

# Having trouble getting studentid and quizid to create as foreign keys, so had to take out
class Scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student = db.Column(db.String, nullable=False)
    quiz = db.Column(db.String, nullable=False)
    score = db.Column(db.Integer, nullable=False)

    def __init__(self, student, quiz, score):
        self.student = student
        self.quiz = quiz
        self.score = score

# This is the login part, currently no authentication
@app.route('/', methods=['POST', 'GET'])
def login():
    title = "Login"
    if request.method == 'POST':
        userid = request.form['userid']
        password = request.form['password']
        if userid == 'admin' and password == 'password':
            return redirect('/dashboard')
        else:
            return render_template("index.html", title=title)
    else:
        return render_template("index.html", title=title)

# This is the dashboard which shows table of students and table of quizzes
@app.route('/dashboard', methods=['POST', 'GET'])
def displayall():
    title = "My Dashboard"
    students = Students.query.order_by(Students.id)
    quizzes = Quizzes.query.order_by(Quizzes.id)
    scores = Scores.query.order_by(Scores.id)
    return render_template("dashboard.html", title=title, students=students, quizzes=quizzes, scores=scores)


@app.route('/addstudent', methods=['POST', 'GET'])
def addstudent():
    title = "Add Student"
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        newstudent = Students(firstname=firstname, lastname=lastname)
        try:
            db.session.add(newstudent)
            db.session.commit()
            return redirect('/addstudent')
        except:
            return "There was an error adding your student"
    else:
        return render_template("addstudent.html", title=title)


@app.route('/addquiz', methods=['POST', 'GET'])
def addquiz():
    title = "Add Quiz"
    if request.method == 'POST':
        subject = request.form['subject']
        qcount = request.form['qcount']
        dategiven = request.form['dategiven']
        newquiz = Quizzes(subject=subject, qcount=qcount, dategiven=dategiven)
        try:
            db.session.add(newquiz)
            db.session.commit()
            return redirect('/addquiz')
        except:
            return "There was an error adding your quiz"
    else:
        return render_template("addquiz.html", title=title)


@app.route('/addgrade', methods=['POST', 'GET'])
def addgrade():
    title = "Add Grade"
    if request.method == 'POST':
        student = request.form['student']
        quiz = request.form['quiz']
        score = request.form['score']
        newgrade = Scores(student=student, quiz=quiz, score=score)
        try:
            db.session.add(newgrade)
            db.session.commit()
            return redirect('/addgrade')
        except:
            return "There was an error adding your grade"
    else:
        students = Students.query.order_by(Students.id)
        quizzes = Quizzes.query.order_by(Quizzes.id)
        return render_template("addgrade.html", title=title, students=students, quizzes=quizzes)


if __name__ == '__main__':
    db.init_app(app)
    db.create_all()
    app.run(debug=True)
