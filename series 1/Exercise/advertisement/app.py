from flask import Flask , render_template , request , redirect , url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#################################################[App instance]#####################################################

app = Flask(__name__)

#################################################[Configurations]####################################################

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
SQLALCHEMY_TRACK_MODIFICATIONS = True

#################################################[Database]####################################################

db = SQLAlchemy(app)

class Advertisement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    contact_phone = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    date = db.Column(db.Date, nullable=False , default=datetime.now)


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False , default=datetime.now)

with app.app_context():
    db.create_all()


#################################################[Views]####################################################

@app.route('/')
def index():
    template_name = 'index.html'
    adds = Advertisement.query.all()
    return render_template(template_name , adds=adds)


@app.route('/add_advertisement' , methods=['GET', 'POST'])
def add_advertisement():
    template_name = 'add_advertisement.html'
    if request.method == 'GET':
        return render_template(template_name)
    elif request.method ==  'POST':
        title = request.form['input_title']
        description = request.form['input_description']
        price = request.form['input_price']
        status = request.form['input_status']
        contact_phone = request.form['input_phone']
        city = request.form['input_city']

        new_add = Advertisement(title=title, description=description, price=price, status=status, contact_phone=contact_phone, city=city)
        db.session.add(new_add)
        db.session.commit()

        return redirect(url_for('index'))


@app.route('/contact' ,methods=['GET', 'POST'])
def contact():
    template_name = 'contact.html'
    if request.method == 'GET':
        return render_template(template_name)
    if request.method == 'POST':
        name = request.form['input_name']
        description = request.form['input_description']
        phone = request.form['input_phone']
        email = request.form['input_email']

        new_ticket = Ticket(name=name, description=description, phone=phone, email=email)
        db.session.add(new_ticket)
        db.session.commit()

        return redirect(url_for('index'))

@app.route('/ad_delete/<int:ad_id>' , methods=['GET', 'POST'])
def ad_delete(ad_id):
    ad = Advertisement.query.get(ad_id)
    db.session.delete(ad)
    db.session.commit()

    return redirect(url_for('index'))
#################################################[Error Handler]####################################################


#################################################[Runtime]####################################################

if __name__ == '__main__':
    app.run(debug=True)
