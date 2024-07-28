from flask import Flask , render_template , request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/shop/<int:shop_id>/<string:shop_name>')
def product_detail(shop_id , shop_name):

    return render_template('detail.html' , product_id = shop_id , product_name = shop_name)


@app.route('/article')
def article():
    return render_template('article.html')