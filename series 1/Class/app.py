from flask import Flask , render_template , request
from flask_sqlalchemy import SQLAlchemy

################################################[Configurations]######################################################

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlite.db"
db = SQLAlchemy(app)

###################################################[DataBase]##########################################################

class Ticket(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String(10))
    lastname = db.Column(db.String(10))
    phone = db.Column(db.String(12))
    body = db.Column(db.String(200))


class Article(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    name_author = db.Column(db.String(10))
    body = db.Column(db.String(200))

with app.app_context():
    db.create_all()

##################################################[Views]##############################################################

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/shop/<int:shop_id>/<string:shop_name>')
def product_detail(shop_id , shop_name):

    return render_template('detail.html' , product_id = shop_id , product_name = shop_name)


@app.route('/articles')
def articles():
    articles = Article.query.all()

    return render_template('article.html', articles=articles)

@app.route('/create_article' , methods=['GET', 'POST'])
def create_article():
    if request.method == 'GET':
        return render_template('create.html')
    elif request.method == 'POST':
        author_name = request.form['input_name']
        body = request.form['input_body']

        new_article = Article(name_author = author_name, body = body)
        db.session.add(new_article)
        db.session.commit()

        return render_template('create.html')

@app.route('/article/<int:article_id>')
def article_detail(article_id):
    #requested_article = Article.query.get(article_id)
    requested_article = db.get_or_404(Article ,article_id)
    return render_template('detail.html' , article = requested_article)


@app.route('/contactus' , methods=['GET', 'POST'])
def contactus():

    if request.method == 'GET' : #IF THE USER VISITED THE PAGE
        print(f'the request containing the get attributes is {request}')
        return render_template('contact_us.html')
    elif request.method == 'POST': #if the user submited a form
        fname = request.form['input_fname']
        lname = request.form['input_lname']
        phone = request.form['input_number']
        body = request.form['input_request']

        new_ticket = Ticket(name = fname, lastname = lname, phone = phone, body = body)
        db.session.add(new_ticket)
        db.session.commit()


        return render_template('contact_us.html')


@app.route('/tickets')
def show_all_tickets():

    tickets = Ticket.query.all()

    return render_template('tickets.html' , tickets=tickets)

################################################[Error Handlers]######################################################

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')

##################################################[Runtime]############################################################

if __name__ == '__main__':
    app.run(debug=True)

