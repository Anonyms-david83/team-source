from flask import Flask , render_template , request
from flask_sqlalchemy import SQLAlchemy


##############################################################

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'



####################################################################


db = SQLAlchemy(app)

with app.app_context():
    db.create_all()


#########################################################################
@app.route('/')
def hello_world():
    return render_template('home.html')




###########################################################################
if __name__ == '__main__':
    app.run()
