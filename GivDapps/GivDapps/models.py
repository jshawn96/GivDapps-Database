from GivDapps import db, app
from sqlalchemy.sql import func
import datetime
import cloudinary.utils

#CodeUpStartTutorial: codeupstart.com/project/build-kickstarter-with-python-and-flask
#Useful ref: http://flask-sqlalchemy.pocoo.org/2.1/models/ ***

#Helper Tables for Many-to-Many Relationships
#This helper table shows all the supporting users for a challenge
challengers = db.Table('challengers',
    db.Column('user_id', db.Integer, db.ForeignKey('User.id')),
    db.Column('challenge_id', db.Integer, db.ForeignKey('Challenge.id'))
)

#This helper table shows all the supporting users for a campaign
users = db.Table('users',
    db.Column('user_id', db.Integer, db.ForeignKey('User.id')),
    db.Column('campaign_id', db.Integer, db.ForeignKey('Campaign.id'))
)

#This helper table shows all the supporting companies for a campaign
companies = db.Table('companies',
    db.Column('company_id', db.Integer, db.ForeignKey('Company.id')),
    db.Column('campaign_id', db.Integer, db.ForeignKey('Campaign.id'))
)

#This is a user.
class User(db.Model):
         __tablename__ = 'User'
        id = db.Column(db.Integer, primary_key=True)

        #Attributes
        first_name = db.Column(db.String(64), nullable=False)
        last_name = db.Column(db.String(64), nullable=False)
        user_email = db.Column(db.String(64), nullable=False)
        password = db.Column(db.String(64), nullable=False)

        #Relationships
        #1. Many users may relate to many campaigns.
            # Uni-direction so nothing here
        #2. One user may relate to many donations.
        donations = db.relationship('Donation', backref='user', lazy='dynamic') #X
        #3. Many users may relate to many challenges.
            # Uni-direction so nothing here
        #4. Many users may relate to one company.
        company_id = db.Column(db.Integer, db.ForeignKey('Company.id')) #X
        #5. Many users may relate to one nonProfit.
        nonProfit_id = db.Column(db.Integer, db.ForeignKey('nonProfit.id'))

#This is a campaign
class Campaign(db.Model):
        __tablename__ = 'Campaign'
        id = db.Column(db.Integer, primary_key=True)

        #Attributes
        campaign_name = db.Column(db.String(64), nullable=False)
        total_goal = db.Column(db.Integer, nullable=False)
        description = db.Column(db.Text, nullable=False)
        category = db.Column(db.String(64), nullable=False)
        tax_deductable = db.Column(db.Boolean(), nullable=False, default=False)
        company_sponsorship = db.Column(db.Boolean(), nullable=False, default=False)
        phone_number = db.Column(db.String(64), nullable=True)
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
        #1. Many users may relate to many campaigns.
        users = db.relationship('User', secondary=users, backref=db.backref('campaigns', lazy='dynamic')) #X
        #2. One campaign may relate to many donations.
        donations = db.relationship('Donation', backref='campaign', lazy='dynamic') #X
        #3. A campaign does not relate to a challenge.
        #4. Many campaigns may relate to many companies.
        companies = db.relationship('Company', secondary=companies, backref=db.backref('campaigns', lazy='dynamic')) #X
        #5. One campaign may relate to one nonProfit.
        nonProfit = db.relationship('nonProfit', backref='campaign', uselist=False, lazy='dynamic') #X


        #Properties
        @property
        def total_donations(self):
            total_donations = db.session.query(func.sum(Donation.amount)).filter(Donation.campaign_id==self.id).one()[0]
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
class Donation(db.Model):
         __tablename__ = 'Donation'
        id = db.Column(db.Integer, primary_key=True)

        #Attributes
        amount = db.Column(db.Integer, nullable=False)
        time_created = db.Column(db.DateTime(timezone=False), nullable=False)

        #Relationships
        #1. One user may relate to many donations.
        user_id = db.Column(db.Integer, db.ForeignKey('User.id')) #X
        #2. One campaign may relate to many donations.
        campaign_id = db.Column(db.Integer, db.ForeignKey('Campaign.id')) #X
        #3. One donation may relate to many challenges.
        challenges = db.relationship('Challenge', backref='donation', lazy='dynamic') #X
        #4. One donation may relate to many companies.
        company_id = db.Column(db.Integer, db.ForeignKey('Company.id')) #X

#This is a challenge.
class Challenge(db.Model):
         __tablename__ = 'Chellenge'
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
        #1. Many users may relate to many challenges.
        challengers = db.relationship('Challenger', secondary=challengers, backref=db.backref('challenges', lazy='dynamic')) #X
        #2. A campaign does not relate to a challenge.
        #3. One donation may relate to many challenges.
        donation_id = db.Column(db.Integer, db.ForeignKey('Donation.id')) #X
        #4. One challenge may relate to one company.
        company = db.relationship('Company', uselist=False, backref='challenge', lazy='dynamic') #X

        @property
        def image_path(self):
            return cloudinary.utils.cloudinary_url(self.photo_link)[0]

#This is a company.
class Company(db.Model):
         __tablename__ = 'Company'
        id = db.Column(db.Integer, primary_key=True)

        #Attributes
        company_name = db.Column(db.String(64), nullable=False)
        street_address = db.Column(db.String(128), nullable=False)
        city = db.Column(db.String(64), nullable=False)
        state = db.Column(db.String(64), nullable=False)
        zip_code = db.Column(db.Integer, nullable=False)
        number_of_employees = db.Column(db.Integer, nullable=False)
        logo_link =  db.Column(db.String(64), nullable=False)
        social_handle = db.Column(db.String(64), nullable=True)
        number_of_donors = db.Column(db.Integer, nullable=True)
        type_of_company = db.Column(db.String(64), nullable=False)
        description = db.Column(db.Text, nullable=False)

        #Propertes
        @property
        def image_path(self):
            return cloudinary.utils.cloudinary_url(self.logo_link)[0]

        #Relationships
        #1. One challenge may relate to one company.
        challenge_id = db.Column(db.Integer, db.ForeignKey('Challenge.id')) #X
        #2. A donation may not relate to a company.
        #3. Many campaigns may relate to many companies.
            #Uni-directional so nothing here
        #4. Many users may relate to one company.
        employees = db.relationship('User', backref='employee', lazy='dynamic') #X

#This is a non-profit company.
class nonProfit(db.Model):
         __tablename__ = 'nonProfit'
        id = db.Column(db.Integer, primary_key=True)

        #Attributes
        nonProfit_name = db.Column(db.String(64), nullable=False)
        street_address = db.Column(db.String(128), nullable=False)
        city = db.Column(db.String(64), nullable=False)
        state = db.Column(db.String(64), nullable=False)
        zip_code = db.Column(db.Integer, nullable=False)
        number_of_employees = db.Column(db.Integer, nullable=False)
        logo_link =  db.Column(db.String(64), nullable=False)
        social_handle = db.Column(db.String(64), nullable=True)
        number_of_donors = db.Column(db.Integer, nullable=True)
        type_of_nonProfit = db.Column(db.String(64), nullable=False)
        description = db.Column(db.Text, nullable=False)

        #Propertes
        @property
        def image_path(self):
            return cloudinary.utils.cloudinary_url(self.logo_link)[0]

        #Relationships
        #1. One campaign may relate to one nonProfit.
        campaign_id = db.Column(db.Integer, db.ForeignKey('Campaign.id')) #X
        #2. A donation may not relate to a nonProfit.
        #3. A challenge may not relate to a nonProfit.
        #4. Many users may relate to one nonProfit.
        employeesNonProfit = db.relationship('User', backref='employee', lazy='dynamic') #X
