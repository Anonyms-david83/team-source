from flask import Flask , render_template , request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

###########################################################################################

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)

############################################################################################


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    subject = db.Column(db.String(80))
    body = db.Column(db.Text)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.Text)
    date = db.Collumn(db.Date , default=datetime.now)


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.Text)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    personel_name = db.Column(db.String(80))
    personel_description = db.Column(db.Text)



with app.app_context():
    db.create_all()

############################################################################################
@app.route('/' , methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact' , methods=['GET', 'POST'])
def contact():

    if request.method == 'GET':
        return render_template('contact.html')
    elif request.method == 'POST':
        name = request.form['input_name']
        email = request.form['input_email']
        subject = request.form['input_subject']
        body = request.form['input_body']


        new_contact = Contact(name=name, email=email, subject=subject, body=body)
        db.session.add(new_contact)
        db.session.commit()
        return render_template('index.html')
@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/testimonial')
def testimonial():
    return render_template('testimonial.html')

###########################################################################################

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')

############################################################################################

if __name__ == '__main__':
    app.run(debug=True)
