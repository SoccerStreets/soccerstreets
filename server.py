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
    loggedin = False
    try:
        session['username']
        loggedin = True
    except:
        loggedin = False

    return render_template(
        'login.html',
        title="SoccerStreets",
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
            session['id'] = user.id
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

@app.route('/checkin', methods=['POST'])
def checkin():
    kid_id = request.form.get('kid_id');
    timestamp = time.time();
    origin =request.form.get('origin');
    destination = request.form.get('destination');
    query = db.insert('chekins',{
    'timestamp' : timestamp,
    'kid_id' : kid_id,
    'chaparone_id' : session[id],
    'origin_id' : origin,
    'dest_id' : destination

    })
        return render_template(
        'checkin_submit.html',
        kid_qr = kid_qr;
        timestamp = timestamp;
        origin = origin;
        destination = destination;
        )
        
@app.route('/checkin5', methods=['POST'])
def checkin5():
        query = db.query("")



@app.route('/checkout', methods=['POST'])
def checkout():
