import bcrypt
from system import db
from models.users import User
from controllers.logger import LoggerController as logger

class UserController():
    def __init__(self):
        self.email = ""
        self.password = ""
        self.api_key = ""
    
    def create_user(self):
        user = User.query.filter_by(email=self.email).first()
        if user:
            return "Email already exists"
        if self.email == True:
            # self.password = bcrypt.generate_password_hash(self.password)
            self.password = bcrypt.hashpw(self.password, bcrypt.gensalt())
            user = User(email=self.email, password=self.password)
            db.session.add(user)
            db.session.commit()
        return "Account created"

    def update_user(self):
        user = User.query.filter_by(email=self.email).first()
        if user:
            if self.email == True:
                self.password = bcrypt.hashpw(self.password, bcrypt.gensalt())
                user.email = self.email
                user.password = self.password
                db.session.commit()
            return "Account updated"
        return "User does not exists"

    def delete_user(self):
        user = User.query.filter_by(email=self.email).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return "Account deleted"
        return "User does not exists"

    def fetch_user_data(self):
        user = User.query.filter_by(email=self.email).first()
        if user:
            self.password = user.password
            self.email = user.email
            return self
        return "User does not exists"

    def authorize_user(self, url):
        return True

    def authenticate_user(self, api_key):
        return True
    
    # def login_user(self):
    #     pass

    # def logout_user(self):
    #     pass