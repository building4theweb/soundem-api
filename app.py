import dotenv


dotenv.read_dotenv()

from flask.ext.script import Manager, prompt, prompt_bool, prompt_pass
from soundem import app, db, fixtures
from soundem.models import User


manager = Manager(app)


@manager.command
def recreate_db(confirm=False):
    """
    Recreates database tables
    """
    if confirm or prompt_bool("Do you want to drop existing data?"):
        print "Dropping..."
        db.drop_all()

    print "Creating..."
    db.create_all()


@manager.command
def populate_db(confirm=False):
    """
    Populates database with sample data
    """
    recreate_db(confirm)

    print "Populating..."

    fixtures.sample()


@manager.command
def create_user():
    email = prompt('Email address')
    password = prompt_pass('Password')

    try:
        print "Creating user..."
        User.create(email, password)
    except:
        print "Error creating user!"


if __name__ == '__main__':
    manager.run()
