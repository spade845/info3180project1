from . import db

class UserProfile(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    age= db.Column(db.Integer)
    gender=db.Column(db.String(6))
    bio=db.Column(db.String(80))
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255))
    image=db.Column(db.LargeBinary)
    created_on=db.Column(db.DateTime)
    
    def __init__(self, uid, firstname, lastname, age, gender, bio, username, password,image, created_on):
        self.uid=uid
        self.firstname=firstname
        self.lastname=lastname
        self.age=age
        self.gender=gender
        self.bio=bio
        self.username=username
        self.password=password
        self.image=image
        self.created_on=created_on
        
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.uid)  # python 2 support
        except NameError:
            return str(self.uid)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)
