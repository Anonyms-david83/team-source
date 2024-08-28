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

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    userphone = db.Column(db.String(20), nullable=False)
    useremail = db.Column(db.String(50), nullable=False)
    userdescription = db.Column(db.String(100), nullable=False)
    useravatar = db.Column(db.String(50), nullable=False)
    adddate = db.Column(db.Date, nullable=False, default=datetime.now)


with app.app_context():
    db.create_all()

########################################################################################################################



class ProfileForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(message='این فیلد نمیتواند خالی باشد') , Length(min=1 , max=20 , message='تعداد کاراکتر غیر مجاز است')] , render_kw={'placeholder': 'Username'})
    userphone = StringField(label='User Phone', validators=[DataRequired(message='این فیلد نمیتواند خالی باشد') , Length(min=1 , max=20 ,message='تعداد کاراکتر غیر مجاز است')] , render_kw={'placeholder': 'User Phone'})
    useremail = EmailField(label='User Email', validators=[DataRequired(message='این فیلد نمیتواند خالی باشد'), Length(min=1 , max=50 ,message='تعداد کاراکتر غیر مجاز است')] , render_kw={'placeholder': 'User Email'})
    userdescription = StringField(label='User Description', validators=[DataRequired(message='این فیلد نمیتواند خالی باشد'), Length(min=10 , max=100 ,message='تعداد کاراکتر غیر مجاز است')] , render_kw={'placeholder': 'User Description'})
    useravatar = FileField(label='User Avatar', validators=[ DataRequired(message='این فیلد نمیتواند خالی باشد'), FileAllowed(['jpg', 'png' , 'jpeg'])] , render_kw={'placeholder': 'User Avatar'})



########################################################################################################################

@app.route('/')
def index():
    template_name = 'index.html'
    profiles = Profile.query.all()
    return  render_template(template_name , profiles=profiles)

@app.route('/register' , methods = ['GET' , 'POST'])
def register():
    template_name = 'register.html'
    form_instance = ProfileForm()
    if request.method == 'GET':
        return render_template(template_name , form=form_instance)
    elif request.method == 'POST':
        if form_instance.validate_on_submit():
            username = form_instance.username.data
            userphone = form_instance.userphone.data
            useremail = form_instance.useremail.data
            userdescription = form_instance.userdescription.data

            useravatar = form_instance.useravatar.data
            filename = secure_filename(useravatar.filename)
            avatar_path = os.path.join(app.config['UPLOADE_PATH'] , filename)

            useravatar.save(avatar_path)

            new_profile = Profile(username=username , userphone=userphone , useremail=useremail , userdescription=userdescription , useravatar=avatar_path)

            db.session.add(new_profile)
            db.session.commit()

            flash('پروفایل شما با موافقیت ثبت شد' , 'success')

            return redirect(url_for('index'))

        else:
            flash('ثبت نام شما با مشکل مواجه شده' , 'warning')
            return render_template(template_name, form=form_instance)


########################################################################################################################

@app.errorhandler(404)
def page_not_found(e):
    template_name = '404.html'
    return render_template(template_name)


########################################################################################################################


if __name__ == '__main__':
    app.run(debug=True)