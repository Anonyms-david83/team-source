from flask import Flask , render_template , request , redirect , url_for
from flask_sqlalchemy import SQLAlchemy

#################################################[App instance]#####################################################

app = Flask(__name__)

#################################################[Configurations]####################################################

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

#################################################[Database]####################################################

db = SQLAlchemy(app)




with app.app_context():
    db.create_all()


#################################################[Views]####################################################

@app.route('/')
def index():
    template_name = 'index.html'
    return render_template(template_name)

#################################################[Error Handler]####################################################


#################################################[Runtime]####################################################

if __name__ == '__main__':
    app.run(debug=True)
