import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()

database_name = os.environ['DB_NAME']
user_name = os.environ['DB_USER']
user_password = os.environ['DB_PASSWORD']
if ((database_name is '' and user_password is '') or (database_name is None and user_password is None)):
    database_path = "postgresql:///{}".format(database_name)
else:
    database_path = "postgresql://{}:{}@{}/{}".format(user_name, user_password, 'localhost:5432', database_name)

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    db.create_all()

class Employee(db.Model):
    __tablename__ = 'Employee'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)

    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname

    def __ref__(self):
        return f'<EMPLOYEE ID: {self.id}, Name: {self.firstname} {self.lastname}>'

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def json_view(self):
        return {
            'id': self.id,
            'first name': self.firstname,
            'last name': self.lastname
        }

class Company(db.Model):
    __tablename__ = 'Company'

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String)
    industry = db.Column(db.String)

    def __init__(self, company_name, industry):
        self.company_name = company_name
        self.industry = industry

    def __ref__(self):
        return f'<COMPANY ID: {self.id}, Name: {self.company_name}, Industry: {self.industry}>'

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def json_view(self):
        return {
            'id': self.id,
            'company name': self.company_name,
            'industry': self.industry
        }

class Works(db.Model):
    __tablename__ = 'Works'

    id = db.Column(db.Integer, primary_key=True)

    employee_id = db.Column(db.Integer, db.ForeignKey('Employee.id'), nullable=False)
    employee = db.relationship('Employee', backref='works')
    company_id = db.Column(db.Integer, db.ForeignKey('Company.id'), nullable=False)
    company = db.relationship('Company', backref='works')

    def __init__(self, employee_id, company_id):
        self.employee_id = employee_id
        self.company_id = company_id

    def __ref__(self):
        return f'<WORKS ID: {self.id}, Employee_Id: {self.employee_id}, Company_Id: {self.company_id}>'

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def employee_json_view(self):
        return {
            'employee_id': self.employee_id
        }
    
    def company_json_view(self):
        return {
            'company_id': self.company_id
        }