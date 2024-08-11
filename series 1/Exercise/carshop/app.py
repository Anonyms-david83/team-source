from flask import Flask , render_template , request , redirect , flash , url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from datetime import datetime

from wtforms import StringField , DateTimeField , IntegerField , BooleanField , FileField
from wtforms.validators import DataRequired , Length
from werkzeug.utils import  secure_filename
import os

##############################################[app instance]#######################################################

app = Flask(__name__)

#############################################[configs]########################################################

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SECRET_KEY'] = '1111111112222222222222wwwwwwwwwwwwwwdawdadwdwwdwdwdwwnbfbneawnfgegesngseineasi'
app.config['UPLOADE_PATH'] = 'static/img'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

############################################[database]##############################################################

db = SQLAlchemy(app)


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False , default=datetime.now)
    cylinder =db.Column(db.Integer, nullable=False)
    health = db.Column(db.Boolean, nullable=False)
    country = db.Column(db.String(20), nullable=False)
    img_path = db.Column(db.String(200), nullable=False)





with app.app_context():
    db.create_all()

#############################################[forms]##########################################################

class CarRegisterForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired(message='نباید این فیلد خالی باشد') , Length(min=1 , max=10 , message='تعداد کاراکتر ها بیش از حد مجاز است')] ,
                       render_kw={'placeholder': 'Name'})

    price = IntegerField(label='Price', validators=[DataRequired(message='نباید این فیلد خالی باشد')], render_kw={'placeholder': 'Price'})
    cylinder = IntegerField(label='Cylinder', validators=[DataRequired(message='نباید این فیلد خالی باشد')] , render_kw={'placeholder': 'Cylinder count'})
    health = BooleanField(label='Health', validators=[DataRequired(message='نباید این فیلد خالی باشد')] , render_kw={'placeholder': 'Health'})
    country = StringField(label='Country', validators=[DataRequired(message='نباید این فیلد خالی باشد') , Length(min=1 , max=20 , message='تعداد کاراکتر ها بیش از حد مجاز است')] ,
                          render_kw={'placeholder': 'Country'})
    img = FileField(label='img' , validators=[DataRequired(message='این فیلد نمیتواند خالی باشد')], render_kw={'placeholder': 'img'})
############################################[views]##############################################################


@app.route('/')
def index():
    template_name = 'index.html'
    cars = Car.query.all()
    return render_template(template_name , cars = cars)


@app.route('/register_car' , methods=['GET', 'POST'])
def register_car():
    template_name = 'register.html'
    form_class = CarRegisterForm()
    if request.method == 'GET':
        return render_template(template_name , form = form_class)
    elif request.method == 'POST':

        if form_class.validate_on_submit():

            name = form_class.name.data
            price = form_class.price.data
            cylinder = form_class.cylinder.data
            health = form_class.health.data
            country = form_class.country.data

            img = form_class.img.data
            filename = secure_filename(img.filename)
            img_path = os.path.join(app.config['UPLOADE_PATH'], filename)

            new_car = Car(name = name , price = price , cylinder = cylinder , health = health , country = country , img_path = img_path)

            db.session.add(new_car)
            db.session.commit()

            img.save(img_path)

        else :
            return render_template(template_name , form = form_class)
    return redirect(url_for('index'))

@app.route('/car_detail/<int:car_id>')
def car_detail(car_id):
    car = db.get_or_404(Car , car_id)
    template_name = 'detail.html'
    return  render_template(template_name , car = car)

@app.route('/car_delete/<int:car_id>')
def car_delete(car_id):
    car = db.get_or_404(Car , car_id)
    db.session.delete(car)
    db.session.commit()

    return redirect(url_for('index'))

#########################################[error handler]##########################################
@app.errorhandler(404)
def page_not_found(e):
    template_name = '404.html'
    return render_template(template_name)

############################################[runtime]############################################################

if __name__ == '__main__' :
    app.run(debug=True)

