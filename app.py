from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)   #just referencing this file

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  
#3 slash is relative and 4 is absolute path #tells the app where database is located
#in relative no need to specify exact location and reside in project location

db = SQLAlchemy(app)    #db initialized

#create model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = True)    #text column - 200 chars and should not be left blank
    completed = db.Column(db.Integer, default = 0)  #to ignore, it is never used
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    #return string everytime we create an element
    def __repr__():
        return '<Task %r>' % self.id    #returns id

#index route
@app.route('/', methods = ['POST', 'GET'])      #add methods that route can accept
def index():
    if request.method == 'POST':
        task_content = request.form['content']  #id of form input
        new_task = Todo(content = task_content)
    
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')

        except:
            return 'issue adding task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks = tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)  #get id else 404 error

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Unable to delete'

@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']       #current task content to form input content

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Failed to update'

    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug = True)   #if any error, will show on page