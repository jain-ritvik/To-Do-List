from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, "todo.db")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(150), nullable=False)
    dateCreated = db.Column(db.DateTime, default=datetime.now)
    completed = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method=="POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('home'))
    
    alltodos = Todo.query.all()
    return render_template('index.html', alltodos=alltodos)

@app.route('/delete/<int:sno>', methods=["POST"])
def delete(sno):
    todo = Todo.query.get_or_404(sno)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/complete/<int:sno>', methods=['POST'])
def complete(sno):
    todo = Todo.query.get_or_404(sno)
    todo.completed = True
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/edit/<int:sno>', methods=["GET"])
def edit(sno):
    todo = Todo.query.get_or_404(sno)
    return render_template('edit.html', todo=todo)

@app.route('/edit/<int:sno>', methods=["POST"])
def editSaving(sno):
    todo = Todo.query.get_or_404(sno)
    todo.title = request.form['title']
    todo.desc = request.form['desc']
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/thanks')
def thanks():
    return render_template('thanks.html')

if __name__=="__main__":
    app.run(debug=True)