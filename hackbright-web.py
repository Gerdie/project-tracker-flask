from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/")
def show_home():
    """Show student list and project list"""

    students = hackbright.get_all_students()
    projects = hackbright.get_all_projects()

    return render_template("index.html",
                            students=students,
                            projects=projects)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github', 'jhacks')
    first, last, github = hackbright.get_student_by_github(github)
    projects = hackbright.get_grades_by_github(github)
    return render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github,
                           projects=projects)


@app.route("/project")
def get_project():
    """Show information about a project."""

    title = request.args.get("title")
    project_title, description, max_grade = hackbright.get_project_by_title(title)
    grades = hackbright.get_grades_by_title(title)

    return render_template("project_info.html",
                            project_title=project_title,
                            description=description,
                            max_grade=max_grade,
                            grades=grades)

@app.route("/search")
def get_student_form():
    """Show forms for searching/adding for a student."""

    return render_template("student_search.html")


@app.route("/student-add", methods=["POST"])
def student_add():
    """Add a student"""

    first = request.form.get("first_name")
    last = request.form.get("last_name")
    github = request.form.get("github")

    hackbright.make_new_student(first, last, github)

    return render_template("student_add.html",
                           first=first,
                           last=last,
                           github=github)


@app.route("/project-add", methods=["POST"])
def project_add():
    """Add a project"""

    title = request.form.get("title")
    description = request.form.get("description")
    max_grade = request.form.get("max_grade")

    hackbright.make_new_project(title, description, max_grade)

    return render_template("project_add.html",
                           title=title,
                           description=description,
                           max_grade=max_grade)


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
