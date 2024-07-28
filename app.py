from flask import Flask , render_template , request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlite.db"
db = SQLAlchemy(app)


class Ticket(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String(10))
    lastname = db.Column(db.String(10))
    phone = db.Column(db.String(12))
    body = db.Column(db.String(200))

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/shop/<int:shop_id>/<string:shop_name>')
def product_detail(shop_id , shop_name):

    return render_template('detail.html' , product_id = shop_id , product_name = shop_name)


@app.route('/article')
def article():
    return render_template('article.html')

@app.route('/article/<int:article_id>/<string:article_slug>')
def article_detail(article_id , article_slug):
    return render_template('detail.html' , a=article_id , b=article_slug)


@app.route('/contactus' , methods=['GET', 'POST'])
def contactus():

    if request.method == 'GET' : #IF THE USER VISITED THE PAGE
        print(f'the request containing the get attributes is {request}')
        return render_template('contact_us.html')
    elif request.method == 'POST': #if the user submited a form
        print(f'the request containing the post attributes is {request}')
        print(request.form['input_fname'])
        print(request.form['input_lname'])
        print(request.form['input_number'])
        print(request.form['input_request'])
        return render_template('contact_us.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')


if __name__ == '__main__':
    app.run(debug=True)

