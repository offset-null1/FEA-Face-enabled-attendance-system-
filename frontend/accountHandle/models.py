from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
db = SQLAlchemy()

class User(UserMixin ,db.Model):
    """ An admin (teachers) cabable to view/edit reports registered students can only read 

        :param str email : valid email address
        :param str password : encrypted valid password of the user
    
    """
    
    __tablename__ : 'user'
    
    
    email = db.Column(db.String, 
        primary_key=True
    )
    
    password = db.Column(db.String, 
        nullable=False, 
        unique=False
    )
    
    user_name = db.Column(db.String, 
        unique=True, 
        nullable=False
    )
    
    name = db.Column(db.String, 
        nullable=False, 
        unique=False
    )
    
    authenticated = db.Column(
        db.Boolean, 
        default=False
    )
    
     created_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )
     
    last_login = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )
    
    # def is_active(self):
    #     """ As all users are active """
    #     return True
    
    # def get_id(self):
    #     return self.email
    
    # def is_anonymous(self):
    #     return False
    
    def set_password(self,password):
        self.password = generate_password_hash(
            password,
            method = 'sha256'
        )
        
    def check_password(self, password):
        """ Check hashed password """
        return check_password(self.password, password)
    
    def __repr__(self):
        return f'User{self.name}'
    
    # @login_manager.user_loader
    # def user_loader(user_id):
    #     """ return user obj associated with user_id(email) """
    #     return user.query.get(user_id)