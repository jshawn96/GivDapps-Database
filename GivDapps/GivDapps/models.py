from GivDapps import db, app
from sqlalchemy.sql import func
import datetime
import cloudinary.utils

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    user_email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64), nullable=False)

    campaign = db.relationship('Campaign', backref='creator', lazy='dynamic')
    donations = db.relationship('Donation', backref='member', lazy='dynamic', foreign_keys='Donation.user_id')
    challenges = db.relationship('Challenge', backref='challenger', lazy='dynamic', foreign_keys='Challenge.user_id')
    company = db.relationship('Company', backref='employee', lazy='dynamic')

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

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

    image_filename = db.Column(db.String(128), nullable=False)

    time_created = db.Column(db.DateTime(timezone=False), nullable=False)
	time_start = db.Column(db.DateTime(timezone=False), nullable=False)
	time_end = db.Column(db.DateTime(timezone=False), nullable=False)

    donations = db.relationship('Donation', backref='campaign', lazy='dynamic', foreign_keys='Donation.campaign_id')

    @property
	def donations(self):
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
		return int(self.total_pledges  * 100 / self.total_goal)

	@property
	def image_path(self):
	    return cloudinary.utils.cloudinary_url(self.image_filename)[0]

class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
	amount = db.Column(db.Integer, nullable=False)
	time_created = db.Column(db.DateTime(timezone=False), nullable=False)

class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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
    id = db.Column(db.Integer, primary_key=True)
	company_name = db.Column(db.String(64), nullable=False)

    street_address = db.Column(db.String(128), nullable=False)
    city = db.Column(db.String(64), nullable=False)
    state = db.Column(db.String(64), nullable=False)
    zip_code = db.Column(db.Integer, nullable=False)

    type_of_business db.Column(db.String(64), nullable=False)
    number_of_employees = db.Column(db.Integer, nullable=False)
    logo_link =  db.Column(db.String(64), nullable=False)
