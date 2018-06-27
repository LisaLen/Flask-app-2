"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)
    grades_and_titles = hackbright.get_grades_by_github(github)

    html = render_template('student_info.html', 
                            first=first,
                            last=last,
                            github=github,
                            grades_and_titles=grades_and_titles)

    return html

@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template('student_search.html')

@app.route("/add_student")
def add_student():
    return render_template('add_student.html')

@app.route("/new-student", methods=["POST"])
def new_student():
    fname = request.form.get('fname')
    lname= request.form.get('lname')
    github = request.form.get('github')
    new_student = hackbright.make_new_student(fname, lname, github)

    
    return render_template('success.html')

@app.route("/project")
def get_project_info():
    title = request.args.get('title')

    project_info = hackbright.get_project_by_title(title)
    students = hackbright.get_grades_by_title(title)
    students_name_grade=[]
    for student in students:
        github = student[0]
        grade = student[1]
        student_name = hackbright.get_student_by_github(github)[0]
        students_name_grade.append((student_name, grade))

    return render_template('project_info.html', project_info=project_info,
                                                student_names = students_name_grade)



if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
