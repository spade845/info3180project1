"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from forms import LoginForm
from forms import CreateUserForm
from models import UserProfile
import random 
import os
from werkzeug import secure_filename
from datetime import date, datetime
from time import strftime





###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        
        # change this to actually validate the entire form submission
        # and not just one field
        username=form.username.data
        password=form.password.data;
        user=UserProfile.query.filter_by(username=username,password=password).first()
            
            
        if user is not None:
            login_user(user)
            
            return redirect(url_for('securepage'))
            
        else:
            flash('ERROR GET AWAY','danger')
            return redirect(url_for("home")) 
            
    flash_errors(form)           
    return render_template("login.html", form=form)
    
@app.route("/profile", methods=["GET", "POST"])
def createuser():
    form = CreateUserForm()
    if request.method == "POST":
        # change this to actually validate the entire form submission
        # and not just one field
        
        uid = random.randint(1,1000)
        firstname = form.firstname.data
        lastname = form.lastname.data
        age= form.age.data
        gender=form.gender.data
        bio=form.bio.data
        username = form.username.data
        password=form.password.data
        file=request.files['image']
        image=secure_filename(file.filename)
        created_on=datetime.now().strftime("%a, %d %b %Y")
        file.save(os.path.join("app/static/images",image))
        user=UserProfile(uid,firstname,lastname,age,gender,bio,username,password,image,created_on)
        db.session.add(user)
        db.session.commit()
            
        
        flash('USER CREATED SUCESSFULLY', 'success')
        
        return redirect(url_for('createuser')) 
                
    flash_errors(form)           
    return render_template('createuser.html', form=form)
    
def flash_errors(form):
    for field, errors in form.errors.items():
        
        for error in errors:
            flash(u"Error in the %s field - %s" % (getattr(form, field).label.text,error), 'danger')    
    



@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')

@app.route('/securepage/')
@login_required
def securepage():
    return render_template('securepage.html')



    
@app.route('/profiles/', methods=["GET", "POST"])

def profiles():
    user=db.session.query(UserProfile).all()
    if request.headers['Content-Type']=='application/json' or request.method=="POST":
        mylist=[]
        for user in user:
            mylist.append({'username': user.username,'userid': user.uid})
            user = {'user': mylist}
        return jsonify(user)
   
    return render_template('profiles.html', user=user)  



@app.route('/profile/<uid>', methods=["POST","GET"] )
def profile(uid):
    user=UserProfile.query.filter_by(uid=uid).first()
    img=url_for('static',filename='images/'+ user.image)
    if request.headers['Content-Type']=='application/json' or request.method=="POST":
        return jsonify(uid=user.uid,username=user.username,age=user.age,gender=user.gender,bio=user.bio,password=user.password,image=user.image,created_on=user.created_on)
    else:
        data={'uid':user.uid,'firstname':user.firstname,'lastname':user.lastname,'username':user.username,'age':user.age,'gender':user.gender,'bio':user.bio,'password':user.password,'image':img,'created_on':user.created_on}
        return render_template('profile.html',data=data)
        
        
    
    """Render website's profile page."""
    return render_template('profile.html')
    
@app.route('/logout/')
@login_required
def logout():
    logout_user()
    """Render the website's profile page."""
    return redirect (url_for('home') )


@login_manager.user_loader
def load_user(uid):
    return UserProfile.query.get(int(uid))

###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
