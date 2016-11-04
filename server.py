from flask import Flask, redirect, render_template, request, session, flash, url_for, send_from_directory
# from flask.ext.qrcode import QRcode
import markdown
from werkzeug import secure_filename
import pg
import time
from dotenv import load_dotenv, find_dotenv
import os
# import requests



load_dotenv(find_dotenv())
tmp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask('SoccerStreets',template_folder=tmp_dir)
# QRcode(app)
app.secret_key = "ksajoivnvaldksdjfj"
db = pg.DB(
    dbname=os.environ.get('PG_DBNAME'),
    host=os.environ.get('PG_HOST'),
    user=os.environ.get('PG_USERNAME'),
    passwd=os.environ.get('PG_PASSWORD')
)

#code for file upload

app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


#for a given file determine whether it's an allowed type or not

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


# Renders Homepage (login and register)
@app.route('/')
def render_homepage():
    return render_template(
        'homepage.html'
            )

# Renders Login page (login form)
@app.route('/login')
def render_login():
    return render_template(
        'login.html'
            )

# Renders Login page (login form)
@app.route('/register')
def render_register():
    query = db.query('Select * from stations').namedresult();
    return render_template(
        'register.html',
        query = query,
    )

@app.route('/submit_login', methods=['POST'])
def submit_login():
    uname = request.form.get('uname')
    pws = request.form.get('pws')
    results = db.query("select * from individuals where uname = $1", uname).namedresult()
    print results[0]
    if len(results) > 0:
        user = results[0]
        if user.pws == pws and user.uname == uname:
            session['id'] = user.id
            session['username'] = user.uname
            session['firstname'] = user.firstname
            session['lastname'] = user.lastname
            flash("Successfully Logged In")
            return redirect('/'+ user.type + '/' + str(user.id))
        flash("Couldn't Log In")
    return redirect('/')

@app.route('/log_out', methods=['POST'])
def log_out():
   del session['id']
   del session['username']
   del session['firstname']
   del session['lastname']
   flash("Successfully Logged Out")
   return redirect('/')

@app.route('/submit_register', methods=['POST'])
def submit_register():
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        img = file.read();

    fname = request.form.get('fname');
    lname = request.form.get('lname');
    phone = request.form.get('phone');
    station = request.form.get('station_id');
    breeze = request.form.get('breeze');
    # address = request.form.get('address');
    parentid = request.form.get('parentid');
    uname = request.form.get('uname');
    pws = request.form.get('pws');
    radio = request.form.get('optradio');
    db.insert('individuals',{
    'lastname' : lname,
    'firstname' : fname,
    'uname' : uname,
    'pws' : pws,
    'type' : radio,
    })
    db.insert('images',{
    'image':img,
    })
    query = db.query("Select id from individuals where uname = $1",uname).namedresult()[0];
    if radio == 'kid':
        db.insert('kids_breeze',{
        'kid_id' : query.id,
        'breeze' : breeze,
        'station_id' : station,
        })
        db.insert('kids_parents',{
        'kid_id' : query.id,
        'parent_id' : parentid,
        })
        db.insert('phonenums',{
        'individ_id' : query.id,
        'phone' : phone,
        })
        return redirect('/'+ radio + '/' + str(query.id))
    elif radio == 'parent':
        db.insert('phonenums',{
        'individ_id' : query.id,
        'phone' : phone,
        })
        return redirect('/'+ radio + '/' + str(query.id))
    elif radio == 'chaperone':
        db.insert('phonenums',{
        'individ_id' : query.id,
        'phone' : phone,
        })
        return redirect('/'+ radio + '/' + str(query.id))

# Renders Individual User Page for KIDS
@app.route('/parent/<parent_id>')
def render_parent(parent_id):
    # Query to get parent information
    parent = db.query('select individuals.firstname from individuals inner join phonenums on individuals.id = phonenums.individ_id where individuals.id = $1', parent_id).namedresult()[0]

    # Query to get all the parent's kids
    kids_list = db.query("select kids.id as kid_id, kids.firstname as kid_fname, kids.lastname as kid_lname from individuals as parents inner join kids_parents on parents.id = kids_parents.parent_id inner join individuals as kids on kids_parents.kid_id = kids.id where parents.id = $1", parent_id).namedresult()

    return render_template(
        'parent.html',
        parent_id = parent_id,
        parent = parent,
        kids_list = kids_list
    )

# Renders Individual User Page for KIDS
@app.route('/kid/<kid_id>')
def render_kid(kid_id):
    return render_template(
        'kid.html',
    )


# Renders Individual User Page for CHAPERONES
@app.route('/chaperone/<chaperone_id>')
def render_chaperone(chaperone_id):
    # Query to get chaperone information
    chaperone = db.query("select distinct on(f_name) individuals.firstname as f_name, phonenums.phone as phone_num from individuals inner join phonenums on individuals.id = phonenums.individ_id where individuals.id = $1", chaperone_id).namedresult()[0]
    query1 = db.query("Select * from stations").namedresult();
    # #Query to get chaperone photo
    # pic = db.query("select picture.file as photo from pictures inner join pictures_individ on pictures.id = pictures_individ.picture_id inner join indviduals on pictures_individ.individ_id = individuals.id where individuals.id = $1", chaperone_id).namedresult()[0].photo

    query2 = db.query("select kids.firstname as kid_fname, kids.lastname as kid_lname, phonenums.phone as parent_phone, parents.firstname as pfname from individuals as chaperones inner join checkins on chaperones.id = checkins.chaperone_id inner join individuals as kids on checkins.kid_id = kids.id  inner join kids_parents on kids.id = kids_parents.kid_id inner join individuals as parents on kids_parents.parent_id = parents.id inner join phonenums on parents.id = phonenums.individ_id where checkins.timestamp >= NOW() - '1 hour'::INTERVAL;").namedresult()
    print query2
    return render_template(
        'chaperone.html',
        phone = chaperone.phone_num,
        query1 = query1,
        query2 = query2
)

@app.route('/chap_checkin_submit', methods=['POST'])
def checkin():
    kid_id = request.form.get('kid_id');
    timestamp = time.time();
    origin_id = request.form.get('origin_id');
    destination_id = request.form.get('destination_id')
    chaperone_id = request.form.get('chaperone_id')
    r = requests.post('https://intense-shore-33606.herokuapp.com/api/v1/checkins', data={'participant_id':kid_id, 'timestamp': timestamp, 'chaperone_id': chaperone_id, 'origin_id':origin_id, 'destination_id': destination_id})
    flash("Checkin Success")
    return redirect ('/chaperone/' + chaperone_id)

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
    app.config['TEMPLATE_AUTO_RELOAD'] = True
    app.run(debug=True)
