import dotenv


dotenv.read_dotenv()

from flask.ext.script import Manager, prompt_bool
from soundem import app, db, fixtures


manager = Manager(app)


@manager.command
def recreate_db():
    """
    Recreates database tables
    """
    if prompt_bool("Do you want to drop existing data?"):
        print "Dropping..."
        db.drop_all()

    print "Creating..."
    db.create_all()


@manager.command
def populate_db():
    """
    Populates database with sample data
    """
    recreate_db()

    print "Populating..."

    fixtures.sample()


if __name__ == '__main__':
    manager.run()
