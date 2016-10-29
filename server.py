from flask import Flask, redirect, render_template, request, session, flash
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

@app.route('/register')
def render_register():
    return render_template(
        'register.html'
    )

# @app.route('/chooseUserType')
# def render_userform():
#     userType = request.form.get('userType')
#     if userType == 'chaperone'
#         return render_template (
#         'chaperone_signup.html'
#         )
#     elif userType == 'parent'
#         return render_template (
#         'parent_signup.html'
#         )
#     else
#         return render_template (
#         'kid_signup.html'
#         )


@app.route('/submit_register')
def submit_register():
    fname = request.form.get('fname');
    lname = request.form.get('lname');
    phone = request.form.get('phone');
    station = request.form.get('station');
    breeze = request.form.get('breeze');
    address = request.form.get('address');
    uname = request.form.get('uname');
    pws = request.form.get('pws');
    radio = request.form.get('optradio');
    db.insert('individuals',{
    'lastname' : lname,
    'firstname' : fname,
    })
    query = db.query("Select id from individuals where uname = $1",uname);
    if radio == 'kid':
        db.insert('')




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
    return render_template (
    'checkin_submit.html',
    kid_qr = kid_qr,
    timestamp = timestamp,
    origin = origin,
    destination = destination
    )

@app.route('/checkin5', methods=['POST'])
def checkin5():
    query = db.query("")
    return redirect('/login')

@app.route('/checkout', methods=['POST'])
def checkout():
    return redirect('/login')

@app.route('/parent')
def render_parent():
    # Query to get all the parent's kids
    kids_list = db.query('')
    return render_template(
        'parent.html',
        kids_list = kids_list
    )

@app.route('/chaperone')
def render_chaperone():
    return render_template(
        'chaperone.html'
    )

@app.route('/kid')
def render_kid():
    # kids_list =
    return render_template(
        'kid.html'
    )


@app.route('/upload', methods=['POST'])
def upload():
    file_name_size = 15
    user_id = request.form.get("id")
    print "user id %s\n\n\n" % user_id
    project_id = request.form.get("project_id")
    print "project id %s\n\n\n" % project_id
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        file_extension = filename.rsplit('.', 1)[1]
        # Create new random name for the file using letters and digits
        filename = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(file_name_size)]) + "." + file_extension
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Redirect the user to the uploaded_file route, which
        # will basically show on the browser the uploaded file
        if user_id:
            db.update (
                "users", {
                    "id": user_id,
                    "avatar": filename
                }
            )
        elif project_id:
            db.insert (
                "image",
                image = filename,
                project_id = project_id
            )
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
