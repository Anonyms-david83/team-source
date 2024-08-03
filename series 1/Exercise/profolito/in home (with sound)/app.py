from flask import Flask , render_template , request , redirect , url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#############################################[App instance]###############################################

app = Flask(__name__)

#############################################[Configurations]###############################################

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

#############################################[Database]###############################################

db = SQLAlchemy(app)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    value = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False , default=datetime.now)

    def __repr__(self):
        return self.name

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    level = db.Column(db.Integer, nullable=False)


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    date = db.Column(db.Date, nullable=False , default=datetime.now)
    phone = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(80), nullable=False)

with app.app_context():
    db.create_all()

#############################################[Views]###############################################

@app.route('/')
def index():
    template_name = 'index.html'
    projects = Project.query.all()
    skills = Skill.query.all()

    return render_template(template_name , projects = projects , skills = skills)


@app.route('/add_project' , methods=['GET', 'POST'])
def add_project():
    template_name = 'add_project.html'
    if request.method == 'GET':
        return render_template(template_name)
    elif request.method == 'POST':
        input_name = request.form.get('input_name')
        input_description = request.form['input_description']
        input_value = request.form.get('input_value')

        new_project = Project(name=input_name, description=input_description, value=input_value)
        db.session.add(new_project)
        db.session.commit() #save

        #return redirect('/')
        return redirect(url_for('index'))


@app.route('/projects')
def projects():
    template_name = 'projects.html'
    projects = Project.query.all()
    return render_template(template_name , projects = projects)


@app.route('/project_detail/<int:project_id>')
def project_detail(project_id):
    template_name = 'project_detail.html'
    project = db.get_or_404(Project , project_id)
    return render_template(template_name , project=project)

@app.route('/add_skill', methods=['GET', 'POST'])
def add_skill():
    template_name = 'add_skill.html'
    if request.method == 'GET':
        return render_template(template_name)
    if request.method == 'POST':
        input_name = request.form.get('input_name')
        input_description = request.form['input_description']
        input_level = request.form.get('input_level')

        new_skill = Skill(name=input_name, description=input_description, level=input_level)
        db.session.add(new_skill)
        db.session.commit()

        return redirect(url_for('index'))

@app.route('/skills')
def skills():
    template_name = 'skills.html'
    skills = Skill.query.all()
    return render_template(template_name , skills = skills)


@app.route('/skill_detail/<int:skill_id>')
def skill_detail(skill_id):
    template_name = 'skill_detail.html'
    skill = db.get_or_404(Skill , skill_id)
    return render_template(template_name , skill=skill)


@app.route('/contactus' , methods=['GET', 'POST'])
def contactus():
    template_name = 'contactus.html'
    if request.method == 'GET':
        return render_template(template_name)
    if request.method == 'POST':
        name = request.form.get('input_fname')
        lastname = request.form.get('input_lname')
        email = request.form.get('input_email')
        phone = request.form.get('input_phone')
        description = request.form.get('input_body')

        new_ticket = Ticket(name=name, last_name=lastname, email=email, phone=phone, description=description)
        db.session.add(new_ticket)
        db.session.commit()

        return redirect(url_for('index'))

#############################################[Error Handler]###############################################

@app.errorhandler(404)
def page_not_found(e):
    template_name = '404.html'
    return render_template(template_name)

#############################################[Runtime]###############################################

if __name__ == '__main__':
    app.run(debug=True)