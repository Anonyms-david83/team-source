from flask import Flask , render_template , request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

##############################################################

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'



####################################################################


db = SQLAlchemy(app)




class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True , unique=True)
    body = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.Boolean, default=True)



with app.app_context(): #with context manager must be always after the class of models
    db.create_all()



#########################################################################
@app.route('/' , methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        todos = Todo.query.all()
        return render_template('home.html' , todos = todos)


    elif request.method == 'POST':
        todo_body = request.form['input_body']
        new_todo = Todo(body=todo_body , status=True)
        db.session.add(new_todo)
        db.session.commit()
        return render_template('home.html')





###########################################################################
if __name__ == '__main__':
    app.run(debug=True)
