from GivDapps import db, app
from sqlalchemy.sql import func
import datetime
import cloudinary.utils

#Useful ref: http://flask-sqlalchemy.pocoo.org/2.1/models/

#This is a user. 
#1. Many users may relate to many campaigns.
#2. One user may relate to many donations.
#3. Many users may relate to many challenges.
#4. Many users may relate to one company. 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    #Attributes
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    user_email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64), nullable=False)

    #Relationships


#This is a campaign 
#1. Many users may relate to many campaigns.
#2. One campaign may relate to many donations. 
#3. A campaign does not relate to a challenge. 
#4. One campaign may relate to one company.
class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    #Attributes
    campaign_name = db.Column(db.String(64), nullable=False)
    total_goal = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(64), nullable=False)
    tax_deductable = db.Column(db.Boolean(), nullable=False, default=False)
    company_sponsorship = db.Column(db.Boolean(), nullable=False, default=False)
    phone_number = db.Column(db.String(64), nullable=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)    
    email = db.Column(db.String(64), unique=True)
    street_address = db.Column(db.String(128), nullable=True)
    city = db.Column(db.String(64), nullable=False)
    state = db.Column(db.String(64), nullable=False)
    zip_code = db.Column(db.Integer, nullable=True)
    amazon_link = db.Column(db.String(128), nullable=True)
    amazon_quantitiy = db.Column(db.Integer, nullable=True)
    image_filename = db.Column(db.String(128), nullable=False)
    time_created = db.Column(db.DateTime(timezone=False), nullable=False)
    time_start = db.Column(db.DateTime(timezone=False), nullable=False)
    time_end = db.Column(db.DateTime(timezone=False), nullable=False)

    #Relationships
	
	
#This is a donation.
#1. One user may relate to many donations.
#2. One campaign may relate to many donations.
#3. One donation may relate to many challenge.
#4. A donation may not relate to a company.
class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    #Attributes    
    amount = db.Column(db.Integer, nullable=False)
    time_created = db.Column(db.DateTime(timezone=False), nullable=False)

    #Relationships
	
	
#This is a challenge.
#1. Many users may relate to many challenges.
#2. A campaign does not relate to a challenge. 
#3. One donation may relate to many challenge.
#4. One challenge may relate to one company.
class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
   
    #Attributes 
    challenge_name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=False)
    challenge_amount = db.Column(db.Integer, nullable=False)
    tax_deductable = db.Column(db.Boolean(), nullable=False, default=False)
    max_people_allowed = db.Column(db.Integer, nullable=False)
    public_can_help = db.Column(db.Boolean(), nullable=False, default=False)
    time_start = db.Column(db.DateTime(timezone=False), nullable=False)
    time_end = db.Column(db.DateTime(timezone=False), nullable=False)
    photo_link = db.Column(db.String(64), nullable=False)
    logo_link =  db.Column(db.String(64), nullable=False)
	
    #Relationships


#This is a company.
#1. One challenge may relate to one company.
#2. A donation may not relate to a company.
#3. One campaign may relate to one company.
#4. Many users may relate to one company. 
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    #Attributes 
    company_name = db.Column(db.String(64), nullable=False)
    street_address = db.Column(db.String(128), nullable=False)
    city = db.Column(db.String(64), nullable=False)
    state = db.Column(db.String(64), nullable=False)
    zip_code = db.Column(db.Integer, nullable=False)
    type_of_business = db.Column(db.String(64), nullable=False)
    number_of_employees = db.Column(db.Integer, nullable=False)
    logo_link =  db.Column(db.String(64), nullable=False)

    #Relationships
	
	
