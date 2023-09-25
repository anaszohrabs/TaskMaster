from flask import Flask, render_template, url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app) # 4

class Todo(db.Model): # 5
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow) # 6
    



    def __repr__(self):
        return '<Task %r>' % self.id
    




@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content'] # 1
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task) # 2
            db.session.commit() # 3
            return redirect('/') # 4
        except:
            tasks = Todo.query.order_by(Todo.date_created).all()
            return 'There was an issue adding your task'
        
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)
    
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id) # 1  
    try:
        db.session.delete(task_to_delete) # 2
        db.session.commit() # 3
        return redirect('/') # 4
    except:
        return 'There was a problem deleting that task'
    
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id) # 1
    if request.method == 'POST':
        task.content = request.form['content'] # 2
        try:
            db.session.commit() # 3
            return redirect('/') # 4
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)
    
    
if __name__ == '__main__':
    app.run(debug=True) # 2 
    with app.app_context():
        db.create_all()
    