from flask import Flask , render_template , request , url_for , flash , redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import  FlaskForm
from wtforms import StringField, IntegerField , FileField  , BooleanField , DateField , TextAreaField , EmailField
from wtforms.validators import DataRequired
from datetime import datetime

##############################################[App instance]############################################

app  = Flask(__name__)

#############################################[Configs]##################################################

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SECRET_KEY'] = '1111111112222222222222wwwwwwwwwwwwwwdawdawnbfbneawnfgegesngseineasi'

#############################################[Database]##################################################

db = SQLAlchemy(app)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    writer_name = db.Column(db.String(80), nullable=False)
    writer_lname = db.Column(db.String(80), nullable=False)
    writer_email = db.Column(db.String(20) , nullable=False)
    writer_phone = db.Column(db.String(12) , nullable=False)
    ticket_date = db.Column(db.Date, nullable=False, default=datetime.now)

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    author_name = db.Column(db.String(80), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.now)


with app.app_context():
    db.create_all()

#############################################[Forms]##################################################

class ContactUsForm(FlaskForm):
    author_name = StringField(label = 'author_name',validators=[DataRequired()] , render_kw={'placeholder':'Your name'})
    author_lname = StringField(label = 'author_lname' ,validators=[DataRequired()] , render_kw={'placeholder':'Your Lastname'})
    author_email = EmailField(label = 'author_email',validators=[DataRequired()] , render_kw={'placeholder':'Your email'})
    author_phone = StringField(label = 'author_phone',validators=[DataRequired()] , render_kw={'placeholder':'Your phone'})
    ticket_subject = StringField(label = 'ticket_subject',validators=[DataRequired()] , render_kw={'placeholder':'subject'})
    ticket_description = StringField(label= 'ticket_description' ,validators=[DataRequired()] , render_kw={'placeholder':'description'})



class NewsForm(FlaskForm):
    news_title = StringField(label = 'news_title',validators=[DataRequired()] , render_kw={'placeholder':'news_title'})
    news_description = StringField(label='news_description' , validators=[DataRequired()] , render_kw={'placeholder':'news_description'})
    author_name = StringField(label='author_name',validators=[DataRequired()] , render_kw={'placeholder':'author_name'})


#############################################[Views]##################################################

@app.route('/')
def index():
    template_name = 'index.html'
    news = News.query.all()
    return render_template(template_name , news_list = news )

@app.route('/contact' , methods=['POST' , 'GET'])
def contact():
    template_name = 'contact.html'
    form_class = ContactUsForm()
    if request.method == 'GET':
        return render_template(template_name, form=form_class)
    elif request.method == 'POST':

        if form_class.validate_on_submit():

            name = form_class.author_name.data
            lastname = form_class.author_lname.data
            email = form_class.author_email.data
            phone = form_class.author_phone.data
            subject = form_class.ticket_subject.data
            description = form_class.ticket_description.data

            new_ticket =  Ticket(subject = subject , description = description , writer_name = name , writer_lname = lastname , writer_email = email , writer_phone = phone )
            db.session.add(new_ticket)
            db.session.commit()

            return redirect(url_for('index'))

        else:

            return render_template(template_name, form=form_class)


@app.route('/write_news' , methods=['GET', 'POST'])
def write_news():
    template_name = 'write_news.html'
    form = NewsForm()
    if request.method == 'GET':
        return render_template(template_name, form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            name = form.author_name.data
            title = form.news_title.data
            description = form.news_description.data

            new_news = News(title = title , description = description , author_name = name )
            db.session.add(new_news)
            db.session.commit()

            return redirect(url_for('index'))
        else:

            return render_template(template_name, form=form)


@app.route('/news_detail/<int:news_id>')
def news_detail(news_id):
    news = db.get_or_404(News , news_id)
    return render_template('news_detail.html' , news = news)


@app.route('/news_delete/<int:news_id>')
def delete_news(news_id):
    news = db.get_or_404(News , news_id)
    db.session.delete(news)
    db.session.commit()
    return redirect('index')
#############################################[ErroHandeler]##################################################

@app.errorhandler(404)
def error_404(e):
    return render_template('404.html')

#############################################[Runtime]##################################################

if __name__ == '__main__':
    app.run(debug=True)