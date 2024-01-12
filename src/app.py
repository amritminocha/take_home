from flask import Flask
from src.extensions import db
from src.endpoints import home
from src.models import Doctor


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    db.init_app(app)
    # We are doing a create all here to set up all the tables. Because we are using an in memory sqllite db, each
    # restart wipes the db clean, but does have the advantage of not having to worry about schema migrations.
    with app.app_context():
        db.create_all()
        # Insert initial doctors into the database
        if not Doctor.query.filter_by(name="Strange").first():
            strange = Doctor(name="Strange")
            db.session.add(strange)

        if not Doctor.query.filter_by(name="Who").first():
            who = Doctor(name="Who")
            db.session.add(who)

        db.session.commit()
    app.register_blueprint(home)
    return app
