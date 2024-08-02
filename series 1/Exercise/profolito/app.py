from flask import Flask , render_template , request , abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

###########################################[App instance]###############################################

app = Flask(__name__)

################################################[Configs]##################################################

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'


#################################################[Database]####################################################

db = SQLAlchemy(app)


class Porject(db.Model):
    id = db.Column(db.Integer, primary_key=True , unique=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(100),  nullable=False)
    value = db.Column(db.Integer(),  nullable=False)
    date = db.Column(db.Date(), nullable=False , default=datetime.now)

    def __repr__(self):
        return self.name

    #id = Column(Integer, primary_key=True , unique=True)
    #name = Column(String(20), unique=True, nullable=False)
    #description = Column(String(100), unique=True, nullable=False)
    #value = Column(Integer(100), unique=True, nullable=False)

with app.app_context():
    db.create_all()


################################################[Views]#####################################################


@app.route('/')
def index():

    template_name = 'index.html'
    projects = Porject.query.all()

    return  render_template(template_name , projects=projects)



@app.route('/add_project' , methods=['GET', 'POST'])
def add_proejct():

    template_name = 'add_proejct.html'

    if request.method == 'GET':
        return render_template(template_name)
    elif request.method == 'POST':
        input_name = request.form.get('input_name') #request.form['input_name']
        input_description = request.form.get('input_description')
        input_value = request.form.get('input_value')

        new_proejct = Porject(name=input_name, description=input_description, value=input_value)
        db.session.add(new_proejct)
        db.session.commit()


        return render_template(template_name)


##################################################[Runtime]###################################################

if __name__ == '__main__':
    app.run(debug=True)