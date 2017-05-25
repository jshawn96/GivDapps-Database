from punchstarter import db, app
from sqlalchemy.sql import func
import datetime
import cloudinary.utils

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(64), nullable=False)
	last_name = db.Column(db.String(64), nullable=False)
    user_email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64), nullable=False)

class Campaign(db.Model):
    campaign_id = db.Column(db.Integer, primary_key=True)
    campaign_name = db.Column(db.String(64), nullable=False)
    total_goal = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(64), nullable=False)
    tax_deductable = db.Column(db.Boolean(), nullable=False, default=False)
    company_sponsorship = db.Column(db.Boolean(), nullable=False, default=False)

    phone_number = db.Column(db.Integer, nullable=True)
    full_name = db.Column(db.String(128), nullable=True)
    email = db.Column(db.String(64), unique=True)

    street_address = db.Column(db.String(128), nullable=True)
    city = db.Column(db.String(64), nullable=False)
    state = db.Column(db.String(64), nullable=False)
    zip_code = db.Column(db.Integer, nullable=True)

    amazon_link = db.Column(db.String(128), nullable=True)
    amazon_quantitiy = db.Column(db.Integer, nullable=True)

    time_created = db.Column(db.DateTime(timezone=False), nullable=False)
	time_start = db.Column(db.DateTime(timezone=False), nullable=False)
	time_end = db.Column(db.DateTime(timezone=False), nullable=False)

class Donation(db.Model):
    donation_id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, nullable=False)
	campaign_id = db.Column(db.Integer, nullable=False)
	amount = db.Column(db.Integer, nullable=False)
	time_created = db.Column(db.DateTime(timezone=False), nullable=False)

class Challenge(db.Model):
    challenge_id = db.Column(db.Integer, primary_key=True)
    challenge_name = db.Column(db.String(64), nullable=False)
    challenge_amount = db.Column(db.Integer, nullable=False)
    tax_deductable = db.Column(db.Boolean(), nullable=False, default=False)
    max_people_allowed = db.Column(db.Integer, nullable=False)
    public_can_help = db.Column(db.Boolean(), nullable=False, default=False)
    time_start = db.Column(db.DateTime(timezone=False), nullable=False)
    time_end = db.Column(db.DateTime(timezone=False), nullable=False)
    photo_link = db.Column(db.String(64), nullable=False)
    logo_link =  db.Column(db.String(64), nullable=False)

class Company(db.Model):
    company_id = db.Column(db.Integer, primary_key=True)
	company_name = db.Column(db.String(64), nullable=False)

    street_address = db.Column(db.String(128), nullable=True)
    city = db.Column(db.String(64), nullable=False)
    state = db.Column(db.String(64), nullable=False)
    zip_code = db.Column(db.Integer, nullable=True)

    type_of_business db.Column(db.String(64), nullable=False)
    number_of_employees = db.Column(db.Integer, nullable=False)
    logo_link =  db.Column(db.String(64), nullable=False)
