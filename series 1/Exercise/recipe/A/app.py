from flask import Flask , render_template , url_for , request , flash , redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField , FileField , IntegerField , TextAreaField
from wtforms.validators import DataRequired , Length
from flask_wtf.file import FileAllowed
from werkzeug.utils import secure_filename
import  os

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


########################################################################################################################

@app.route('/' , methods=['GET', 'POST'])
def index():
    template_name = 'index.html'

    return render_template(template_name)


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

            flash('رسیپ شما با موفقیت ثبت شد ')

            return redirect(url_for('index'))

        else :

            flash('مشکلی در ثبت رسیپ وجود داشت لطفا دوباره سعی کنید')
            return render_template(template_name , form = form_class)


########################################################################################################################





########################################################################################################################

if __name__ == '__main__':
    app.run(debug=True)
