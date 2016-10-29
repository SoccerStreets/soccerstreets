from flask import Flask, redirect, render_template, request, session, flash
from wiki_linkify import wiki_linkify
import markdown
import pg
import time
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
tmp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask('SoccerStreets', template_folder=tmp_dir)
app.secret_key = "ksajoivnvaldksdjfj"
db = pg.DB(
    dbname=os.environ.get('PG_DBNAME'),
    host=os.environ.get('PG_HOST'),
    user=os.environ.get('PG_USERNAME'),
    passwd=os.environ.get('PG_PASSWORD')
)

@app.route('/')
def render_homepage():
    pages = db.query("select p.pagename, max(c.timestamp) from pages as p, content as c where p.id=c.pageid group by p.pagename").namedresult()
    loggedin = False
    try:
        session['username']
        loggedin = True
    except:
        loggedin = False

    return render_template(
        'homepage.html',
        title="Jesslyn's Wiki",
        pages = pages,
        loggedin = loggedin
    )

@app.route('/submit_login', methods=['POST'])
def submit_login():
    username = request.form.get('username')
    password = request.form.get('password')
    results = db.query("select * from users where username = $1", username).namedresult()
    if len(results) > 0:
        user = results[0]
        if user.password == password:
            session['username'] = user.username
            flash("Successfully Logged In")
            return redirect('/')
        else:
            return redirect('/')
    else:
        return redirect('/')

@app.route('/logout', methods=['POST'])
def logout():
    del session['username']
    flash("Successfully Logged Out")
    return redirect('/')
