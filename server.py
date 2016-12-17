from flask import Flask, redirect, render_template, request, session, flash, url_for, send_from_directory
from base64 import b64encode
from flask_qrcode import QRcode
import markdown
from werkzeug import secure_filename
import pg
import time
from dotenv import load_dotenv, find_dotenv
import os
from PIL import Image
# import requests



load_dotenv(find_dotenv())
tmp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask('SoccerStreets',template_folder=tmp_dir)
QRcode(app)
app.secret_key = "ksajoivnvaldksdjfj"
db = pg.DB(
    dbname=os.environ.get('PG_DBNAME'),
    host=os.environ.get('PG_HOST'),
    user=os.environ.get('PG_USERNAME'),
    passwd=os.environ.get('PG_PASSWORD')
)

#code for file upload
APP_ROOT = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT,'static/uploads')
# UPLOAD_FOLDER = 'Users/keyur/DigitalCrafts/marta/soccerstreets/static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])


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
    if 'id' in session:
        #if already loggedin, redirect to user page
        return redirect('/'+ session['type'] + '/' + str(session['id']))
    else:
        return render_template(
            'login.html'
                )

# Renders Registration page (registration form)
@app.route('/register')
def render_register():
    query = db.query('Select * from stations').namedresult();
    return render_template(
        'register.html',
        query = query,
    )

# Executed from press of "login" button on login page
# Redirects to user page if valid user, otherwise redirects to home
@app.route('/submit_login', methods=['POST'])
def submit_login():
    uname = request.form.get('uname')
    pws = request.form.get('pws')
    user_list = db.query("select i.id as id, i.firstname as fname, i.lastname as lname, i.uname as uname, i.pws as pws, i.type as type, phonenums.phone as phone from individuals as i inner join phonenums on i.id = phonenums.individ_id where uname = $1", uname).namedresult()
    if len(user_list) > 0:
        user = user_list[0]
        if user.pws == pws and user.uname == uname:
            session['id'] = user.id
            session['username'] = user.uname
            session['firstname'] = user.fname
            session['lastname'] = user.lname
            session['phone'] = user.phone
            session['type'] = user.type
            return redirect('/'+ user.type + '/' + str(user.id))
    else:
        flash("Invalid username or password")
        return redirect('/login')

#Logs user out of site and redirects to login page
@app.route('/log_out')
def log_out():
    del session['id']
    del session['username']
    del session['firstname']
    del session['lastname']
    del session['phone']
    del session['type']
    flash("Successfully Logged Out")
    return redirect('/login')

@app.route('/submit_register', methods=['POST'])
def submit_register():
    print 'submitted registration form'
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        im1 = Image.open(file)
        im1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename),quality=20)

        random_name1 = os.urandom(6).encode('hex')
        random_name2 = os.urandom(6).encode('hex')
        random_name = random_name1+'_'+random_name2
        new_name = random_name+'.jpeg'
        old_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        new_file = os.path.join(app.config['UPLOAD_FOLDER'], new_name)
        os.rename(old_file,new_file)

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
    query = db.query("Select id from individuals where uname = $1",uname).namedresult()[0];

    db.insert('images',{
    'image' : new_name,
    'indiv_id' : query.id,
    })

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

# Renders Individual User Page for PARENTS
@app.route('/parent/<parent_id>')
def render_parent(parent_id):
    # Query to get parent information
    parent = db.query('select individuals.firstname from individuals inner join phonenums on individuals.id = phonenums.individ_id where individuals.id = $1', parent_id).namedresult()[0]
    parent_image = db.query("select image from images where indiv_id = $1", parent_id).namedresult()[0].image;

    # Query to get all the parent's kids
    kids_list = db.query("select kids.id as kid_id, kids.firstname as kid_fname, kids.lastname as kid_lname, phonenums.phone as kid_phone from individuals as parents inner join kids_parents on parents.id = kids_parents.parent_id inner join individuals as kids on kids_parents.kid_id = kids.id inner join phonenums on kids.id = phonenums.individ_id where parents.id = $1", parent_id).namedresult()

    kids_trips = [];
    for kid in kids_list:
        try:
            print "entered trip block"
            # Query to get latest checkin for each kid
            current_trip = db.query('select chaperones.id as chap_id, chaperones.firstname as chap_fname, chaperones.lastname as chap_lname, phonenums.phone as chap_phone, checkins.origin_id as origin, checkins.dest_id as destination, checkins.action as action from checkins inner join individuals as chaperones on checkins.chaperone_id = chaperones.id inner join phonenums on chaperones.id = phonenums.individ_id where checkins.kid_id = $1 order by checkins.timestamp limit 1', kid.kid_id).namedresult()[0]
            # Query to get origin station for current_trip
            origin = db.query('select * from stations where stations.id = $1', current_trip.origin).namedresult()[0]
            # Query to get origin station for current_trip
            destination = db.query('select * from stations where stations.id = $1', current_trip.destination).namedresult()[0]
            #Queries to get images for the parent, each of their kids and the chaperone of their kid's current trip
            kid_image = db.query("select image from images where indiv_id = $1", kid.kid_id).namedresult()[0].image;
            chaperone_image = db.query("select image from images where indiv_id = $1", current_trip.chap_id).namedresult()[0].image;

            #Append current trip, origin, and destination to kids_trips
            kids_trips.append([current_trip, origin, destination, kid_image, chaperone_image])
            print kids_trips
        except:
            kids_trips.append(['false'])

    #Zip kids_list and kids_trips
    kids_master = zip(kids_list, kids_trips)

    return render_template(
        'parent.html',
        # parent_id = parent_id,
        parent = parent,
        parent_image = parent_image,
        kids_master = kids_master
    )

# Renders Individual User Page for KIDS
@app.route('/kid/<kid_id>')
def render_kid(kid_id):
    # Query to get latest checkin for kid
    current_trip = db.query('select chaperones.id as chap_id, chaperones.firstname as chap_fname, chaperones.lastname as chap_lname, phonenums.phone as chap_phone, checkins.origin_id as origin, checkins.dest_id as destination, checkins.action as action from checkins inner join individuals as chaperones on checkins.chaperone_id = chaperones.id inner join phonenums on chaperones.id = phonenums.individ_id where checkins.kid_id = $1 order by checkins.timestamp limit 1', kid_id).namedresult()[0]
    # Query to get origin station for current_trip
    origin = db.query('select * from stations where stations.id = $1', current_trip.origin).namedresult()[0]
    # Query to get origin station for current_trip
    destination = db.query('select * from stations where stations.id = $1', current_trip.destination).namedresult()[0]
    # Query to get kid's parent info
    parent = db.query('select parents.id as parent_id, parents.firstname as parent_fname, parents.lastname as parent_lname, phonenums.phone as parent_phone from individuals as kids inner join kids_parents on kids.id = kids_parents.kid_id inner join individuals as parents on kids_parents.parent_id = parents.id inner join phonenums on parents.id = phonenums.individ_id where kids.id = $1', kid_id).namedresult()[0]
    #Queries to get images for kid, their parent, and the chaperone of their current trip
    kid_image = db.query("select image from images where indiv_id = $1", kid_id).namedresult()[0].image
    parent_image = db.query("select image from images where indiv_id = $1", parent.parent_id).namedresult()[0].image
    chaperone_image = db.query("select image from images where indiv_id = $1", current_trip.chap_id).namedresult()[0].image

    return render_template(
        'kid.html',
        kid_id = kid_id,
        current_trip = current_trip,
        origin = origin,
        destination = destination,
        parent = parent,
        kid_image = kid_image,
        parent_image = parent_image,
        chaperone_image = chaperone_image
    )

# Renders Individual User Page for CHAPERONES
@app.route('/chaperone/<chaperone_id>')
def render_chaperone(chaperone_id):
    #Query to get chaperone photo
    image = db.query("select image from images where indiv_id = $1", chaperone_id).namedresult()[0].image;
    # Query to get kids currently under chaperone supervision
    kids_list = db.query(
        "select kids.firstname as kid_fname, kids.lastname as kid_lname, phonenums.phone as parent_phone, parents.firstname as pfname, images.image as kid_image from individuals as chaperones inner join checkins on chaperones.id = checkins.chaperone_id inner join individuals as kids on checkins.kid_id = kids.id inner join kids_parents on kids.id = kids_parents.kid_id inner join individuals as parents on kids_parents.parent_id = parents.id inner join phonenums on parents.id = phonenums.individ_id inner join images on images.indiv_id = kids.id where checkins.timestamp >= NOW() - '1 day'::INTERVAL;").namedresult()

    return render_template(
        'chaperone.html',
        kids_list = kids_list,
        chaperone_image = image
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
