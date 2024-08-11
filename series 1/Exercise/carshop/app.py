from flask import Flask , render_template , request , redirect , flash , url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm

##############################################[app instance]#######################################################

app = Flask(__name__)

#############################################[configs]########################################################

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.secret_key = 'wdiegjnejioionesriognseiofgneiosnfgioesngioesngiongionginerniegnierngsegiongiosenmgioseng'

UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

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

@app.errorhandler(404)
def page_not_found(e):
    template_name = '404.html'
    return render_template(template_name)

############################################[runtime]############################################################

if __name__ == '__main__' :
    app.run(debug=True)

