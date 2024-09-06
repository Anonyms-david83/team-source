from flask import Flask , render_template , request , redirect , flash , url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField , IntegerField  , FileField , EmailField
from wtforms.validators import DataRequired , Length
from datetime import datetime
from werkzeug.utils import secure_filename
import os

########################################################################################################################

app = Flask(__name__)

########################################################################################################################

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SECRET_KEY'] = '1111111112222222222222wwwwwwwwwwwwwwdawdadwdwwdwdwdwwnbfbneawnfgegesngseineasi'
app.config['UPLOADE_PATH'] = 'static/img'


########################################################################################################################

db = SQLAlchemy(app)


class Medicine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    description = db.Column(db.Text , nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    add_date = db.Column(db.Date, nullable=False , default=datetime.now )
    img_path = db.Column(db.String(80), nullable=False)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    date = db.Column(db.Date, nullable=False , default=datetime.now)
    phone = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(80), nullable=False)

with app.app_context():
    db.create_all()

########################################################################################################################

class MedicineForm(FlaskForm):

    name = StringField(label='Medicin Name', validators=[DataRequired(message='این فیلد نمیتواند خالی باشد') , Length( min=1 , max=10 ,
                                                         message='تعداد کاراکتر ها نمیتواند بیشتر از 10 حرف باشد')])

    description = StringField(label='Medicin Description' , validators=[DataRequired(message='این فیلد نمیتواند خالی باشد') , Length( min=10 , max=80 ,
                                                         message='تعداد کاراکتر ها باید بین 10 تا 80 کلمه باشد')])

    price = IntegerField(label='Medicin Price' ,validators=[DataRequired(message='این فیلد نمیتواند خالی باشد')])

    quantity = IntegerField(label='Medicin Quantity' , validators=[DataRequired(message='تعداد دارو ها نمیتواند خالی باشد')])

    img = FileField(label='medicin image' , validators=[DataRequired(message='این فیلد نمیتواند خالی باشد') ,
                                                        FileAllowed(['jpg', 'png','jpeg'], message='فرمت ورودی فقط میتواند jpg یا png باشد ' ,)])


class Ticket(FlaskForm):
    name = StringField(label='Your name' , validators=[DataRequired(message='این فیلد نمیتواند خالی باشد') , Length(min=2 , max=20)])
    lname = StringField(label='Your lname' , validators=[DataRequired(message='این فیلد نمیتواند خالی باشد') , Length(min=2 , max=20)])
    description = StringField(label='Your request' , validators=[DataRequired(message='این فیلد نمیتواند خالی باشد') , Length(min=2 , max=100)])
    phone = IntegerField(label='Your phone' , validators=[DataRequired(message='این فیلد نمیتواند خالی باشد مرد مومن')])
    email = EmailField(label='your email' , validators=[DataRequired(message='این فیلد نمیتواند خالی باشد')])






########################################################################################################################
@app.route('/')
def index():
    template_name = 'index.html'
    medicins = Medicine.query.all()

    return render_template(template_name , medicins=medicins)


@app.route('/medicins')
def medicins():
    template_name = 'medicins.html'
    medicins = Medicine.query.all()
    return render_template(template_name , medicins=medicins)

@app.route('/add_medicin' , methods=['GET', 'POST'])
def add_medicin():
    template_name = 'add_medicin.html'
    form_class = MedicineForm()

    if request.method == 'GET':
        return render_template(template_name , form = form_class )
    elif request.method == 'POST':
        if form_class.validate_on_submit():

            name = form_class.name.data
            description = form_class.description.data
            price = form_class.price.data
            quantity = form_class.quantity.data

            img = form_class.img.data
            filename =  secure_filename(img.filename)
            #img_path = os.path.join('static/img' , filename )
            img_path = os.path.join(app.config['UPLOADE_PATH'], filename)  # static/img/b12.jpg
            #                                                         app.config     |  filename
            img.save(img_path)

            new_medicin = Medicine(name=name , description=description , price=price , quantity=quantity , img_path=img_path)

            db.session.add(new_medicin)
            db.session.commit()

            return redirect(url_for('index'))

        else :
            return render_template(template_name , form = form_class )


@app.route('/medicin_detail/<int:medicin_id>')
def medicin_detail(medicin_id):
    #Medicine.query.get(medicin_id)
    medicin = db.get_or_404(Medicine , medicin_id)
    template_name = 'medicin_detail.html'
    print(medicin.img_path)

    return render_template(template_name , medicin = medicin)


@app.route('/contact' , methods = ['POST' , 'GET'])
def contact():
    template_name = 'contact.html'
    form_class = Ticket()

    if request.method == 'GET':


        return  render_template(template_name , form = form_class)

    elif request.method == 'POST':
        if form_class.validate_on_submit():
            name = form_class.name.data
            lname = form_class.lname.data
            phone = form_class.phone.data
            email = form_class.email.data
            description = form_class.description.data

            new_ticket = Ticket(name=name , lname=lname , phone=phone , email=email , description=description)
            db.session.add(new_ticket)
            db.session.commit()

            return redirect(url_for('index'))

        else :
            return render_template(template_name, form=form_class)


########################################################################################################################



########################################################################################################################

if __name__ == '__main__':
    app.run(debug=True)

