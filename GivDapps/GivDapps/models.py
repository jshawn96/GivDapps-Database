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
    campaigns = db.relationship('Campaign', backref='creator', lazy='dynamic')
    donations = db.relationship('Donate', backref='member', lazy='dynamic', foreign_keys='Donation.member_id')

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
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    donations = db.relationship('Donation', backref='campaign', lazy='dynamic', foreign_keys='Donation.project_id')

    #Properties
    @property
    def total_donations(self):
	total_donations = db.session.query(func.sum(Donation.amount)).filter(Donation.project_id==self.id).one()[0]
	if total_donations is None:
	 	total_donations = 0

	return total_donations

	@property
	def num_donations(self):
		return self.donations.count()

	@property
	def num_days_left(self):
		now = datetime.datetime.now()
		num_days_left = (self.time_end - now).days

		return num_days_left

	@property
	def percentage_funded(self):
		return int(self.total_donations  * 100 / self.total_goal)

	@property
	def image_path(self):
	    return cloudinary.utils.cloudinary_url(self.image_filename)[0]

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
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

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
