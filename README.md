# GivDapps-Database
This repo. is based on codeupstart's project build-kickstarter-with-python-and-flask, altered to work with GivDapps' model.

https://www.codeupstart.com/project/build-kickstarter-with-python-and-flask
Reference: http://flask-sqlalchemy.pocoo.org/2.1/models/

TO DO:
**Add Photo Model
One photo can relate to one campaign, company, challenge, user, nonProfit
Each photo should have an id, a format, and a date created.

**The comments should be specifying the actual relationship verbiage.

lprescott [10:25 PM] 
How to get started on the python data base w/ flask and sql alchemy:
1: Navigate to https://www.codeupstart.com/login
The username and password that you are going to use is as follows: REDACTED and REDACTED. Once logged in, resume Build Kickstarter with Python and Flask. Watch the introduction and setting up the project. 
2: Navigate to https://github.com/lprescott/GivDapps-Database
Become a collaborator/contributor to this repository (message me or by request).
3: Start helping out! Thanks.

I got past the sqlalchemy.exc.NoReferencedTableError by formally declaring each table name in the models. This is the commit in case you are curious: https://goo.gl/t9gDO5. 

Adam has asked me to layout the next steps, so here I go: 
First, only after completing my previous post: How to get started on the python data base w/ flask and sql alchemy, can you start migrating the database on your personal computer. I think this is the best way to make sure any changes you make are correct/able to run. 
Second, to init, migrate, and upgrade on your computer one must delete the migrations folder and app.db file -- otherwise you'll get errors even when the code is correct. 
Third, the goal/what I think needs improvement: **I need people to confirm the logic in the relationships** by referencing the link mentioned previously. **I also need people to confirm the logic in the attributes** and the parameters passed on them, i.e. nullable=True... etc. **The models have very limited properties in some cases, more might need to be added.** depending on what is needed from the front-end. Communication please! 
Fourth, extensive testing on the command line, as shown in the video -- we want the database to be as stable as possible. Fifth, have fun and learn. 
Finally, after that is all done we can start focusing on the concatenation of the font-end and back-end. Thanks!

Commands for Ctrl+Cing:
python manage.py db init
python manage.py db migrate
python manage.py db upgrade

from GivDapps.models import *
from GivDapps import db
user1 = User(first_name = "Luke", last_name = "Creator", user_email = "test@gmail.com", password = "password")
db.session.add(user1)
db.session.commit()
