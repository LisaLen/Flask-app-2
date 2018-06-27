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

@app.route("/homepage")
def get_student_form():
    """Show form for searching for a student."""
    student_names = hackbright.get_all_students()
    project_titles = hackbright.get_all_projects()

    return render_template('homepage.html', 
                            student_names=student_names, project_titles=project_titles)


@app.route("/add_student")
def add_student():
    return render_template('add_student.html')

@app.route("/new-student", methods=["POST"])
def new_student():
    fname = request.form.get('fname')
    lname= request.form.get('lname')
    github = request.form.get('github')
    hackbright.make_new_student(fname, lname, github)

    
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
        students_name_grade.append((student_name, grade, github))

    return render_template('project_info.html', project_info=project_info,
                                                student_names = students_name_grade)

@app.route("/add-project")
def add_project():
    return render_template('add_project.html')

@app.route("/new-project", methods=["POST"])
def new_project():
   title = request.form.get('title')
   description = request.form.get('description')
   max_grade = request.form.get('max_grade')


   hackbright.make_new_project(title, description, max_grade)

   return render_template('project_added.html')




if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
