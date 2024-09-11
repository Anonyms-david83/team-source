from flask import Flask , render_template , url_for , request
from flask_sqlalchemy import SQLAlchemy

########################################################################################################################

app = Flask(__name__)



########################################################################################################################

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'EGJMOOogemogmeomgeopsmoeismgiomo34iwmo3moim22313313232123'
app.config['UPLOAD_DIR'] = 'static/uploads'

########################################################################################################################

db = SQLAlchemy(app)




with app.app_context():
    db.create_all()


########################################################################################################################




########################################################################################################################

@app.route('/' , methods=['GET', 'POST'])
def index():
    template_name = 'index.html'

    return render_template(template_name)




########################################################################################################################





########################################################################################################################

if __name__ == '__main__':
    app.run(debug=True)
