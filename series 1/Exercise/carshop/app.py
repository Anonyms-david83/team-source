from flask import Flask , render_template , request , redirect , flash , url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm

##############################################[app instance]#######################################################

app = Flask(__name__)

#############################################[configs]########################################################

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.secret_key = 'wdiegjnejioionesriognseiofgneiosnfgioesngioesngiongionginerniegnierngsegiongiosenmgioseng'


############################################[database]##############################################################

db = SQLAlchemy(app)








with app.app_context():
    db.create_all()

#############################################[forms]##########################################################




############################################[views]##############################################################


@app.route('/')
def index():
    template_name = 'index.html'

    return render_template(template_name)


#############################################[error handler]######################################################


############################################[runtime]############################################################

if __name__ == '__main__' :
    app.run(debug=True)

