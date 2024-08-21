from flask import Flask , render_template , request , redirect , flash , url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm

########################################################################################################################

app = Flask(__name__)

########################################################################################################################

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SECRET_KEY'] = '1111111112222222222222wwwwwwwwwwwwwwdawdadwdwwdwdwdwwnbfbneawnfgegesngseineasi'


########################################################################################################################

db = SQLAlchemy(app)


with app.app_context():
    db.create_all()

########################################################################################################################

@app.route('/')
def index():
    template_name = 'index.html'

    return render_template(template_name)


########################################################################################################################



########################################################################################################################

if __name__ == '__main__':
    app.run(debug=True)

