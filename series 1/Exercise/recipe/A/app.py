from flask import Flask , render_template , url_for , request , flash , redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField , FileField , IntegerField , TextAreaField , EmailField
from wtforms.validators import DataRequired , Length , Email
from flask_wtf.file import FileAllowed
from werkzeug.utils import secure_filename
import  os
from datetime import datetime

########################################################################################################################

app = Flask(__name__)



########################################################################################################################

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'EGJMOOogemogmeomgeopsmoeismgiomo34iwmo3moim22313313232123'
app.config['UPLOAD_DIR'] = 'static/uploads'

########################################################################################################################

db = SQLAlchemy(app)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True , unique=True)
    name = db.Column(db.String(80), nullable=False)
    country =db.Column(db.String(80), nullable=False)
    ingredients = db.Column(db.String(1000), nullable=False)
    instructions = db.Column(db.String(5000), nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    img_url = db.Column(db.String(50), nullable=False , unique=True)
    add_date = db.Column(db.Date, nullable=False, default=datetime.now)

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

class RecipeRegisterationForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired(message='این فیلد نمیتواند خالی باشد') , Length(min=1 , max=80 ,message='تعداد کاراکتر کوتاه است')])
    country =StringField(label='Country', validators=[DataRequired(message='این فیلد نمیتواند خالی باشد') , Length(min=1 , max=80 ,message='تعداد کاراکتر کوتاه است')])
    ingredients = TextAreaField(label='Ingredients', validators=[DataRequired(message='این فیلد نمیتواند خالی باشد') , Length(min=1 , max=1000 ,message='تعداد کاراکتر کوتاه است')])
    instructions = TextAreaField(label='Instructions', validators=[DataRequired(message='این فیلد نمیتواند خالی باشد') , Length(min=1 , max=5000 ,message='تعداد کاراکتر کوتاه است')])
    cost = IntegerField(label='Cost', validators=[DataRequired(message='این فیلد نمیتواند خالی باشد')])
    img = FileField(label='Image URL', validators=[DataRequired(message='این فیلد نمیتواند خالی باشد') , FileAllowed(['jpg', 'png','jpeg'], message='فرمت ورودی فقط میتواند jpg یا png باشد ')])

class TicketForm(FlaskForm):
    name = StringField(label='Your name' , validators=[DataRequired(message='این فیلد نمیتواند خالی باشد') , Length(min=2 , max=20)])
    lname = StringField(label='Your lname' , validators=[DataRequired(message='این فیلد نمیتواند خالی باشد') , Length(min=2 , max=20)])
    description = StringField(label='Your request' , validators=[DataRequired(message='این فیلد نمیتواند خالی باشد') , Length(min=2 , max=100)])
    phone = IntegerField(label='Your phone' , validators=[DataRequired(message='این فیلد نمیتواند خالی باشد مرد مومن')])
    email = EmailField(label='your email' , validators=[DataRequired(message='این فیلد نمیتواند خالی باشد') , Email(message='ایمیل وارد شده مشکل داره')])

########################################################################################################################

@app.route('/' , methods=['GET', 'POST'])
def index():
    template_name = 'index.html'
    recipes = Recipe.query.all()
    form_class = TicketForm()

    return render_template(template_name , recipes = recipes , form = form_class)


@app.route('/register' , methods=['GET', 'POST'])
def register():
    form_class = RecipeRegisterationForm()
    template_name = 'register.html'

    if request.method == 'GET':
        return render_template(template_name , form=form_class)
    elif request.method == 'POST':
        if form_class.validate_on_submit():
            name = form_class.name.data
            country = form_class.country.data
            ingredients = form_class.ingredients.data
            instructions = form_class.instructions.data
            cost = form_class.cost.data

            img = form_class.img.data
            filename = secure_filename(img.filename)

            img_url = os.path.join(app.config['UPLOAD_DIR'], filename) #static/img/b12.jpg
            #                                                         upload_dir  |  filename

            new_recipe = Recipe(name = name , country = country , ingredients = ingredients , instructions = instructions , cost = cost , img_url = img_url )
            db.session.add(new_recipe)
            db.session.commit()

            img.save(img_url)

            flash('رسیپ شما با موفقیت ثبت شد ' , 'success')

            return redirect(url_for('index'))

        else :

            flash('مشکلی در ثبت رسیپ وجود داشت لطفا دوباره سعی کنید' , 'danger')
            return render_template(template_name , form = form_class)

@app.route('/detail/<int:recipe_id>')
def detail(recipe_id):
    target_recipe = db.get_or_404(Recipe , recipe_id)
    template_name = 'detail.html'
    return render_template(template_name , recipe = target_recipe)

@app.route('/delete/<int:recipe_id>')
def delete(recipe_id):
    target_recipe = db.get_or_404(Recipe , recipe_id)
    # target_recipe = Recipe.get_or_404(recipe_id)

    try:
        db.session.delete(target_recipe)
        img_path = target_recipe.img_url
        os.remove(img_path)
        db.session.commit()
        flash('با موفقیت غذای بد مزه شما حذف شد' , 'success')
        return redirect(url_for('index'))
    except:
        flash('اینقدر غذات نحذ بود پاک نشد دوباره امتحان کن' , 'success')
        return redirect(url_for('index'))


@app.route('/contactus' , methods = ['POST' , 'GET'])
def contactus():
    template_name = 'contact.html'
    form_class = TicketForm()

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
            flash('تیکت با موفقیت ثبت شد ' , 'success')

            return redirect(url_for('index'))

        else :
            return render_template(template_name, form=form_class)
            flash('تیکت مشکل داشت دوباره امتحان کنید' , 'error')

########################################################################################################################





########################################################################################################################

if __name__ == '__main__':
    app.run(debug=True)
