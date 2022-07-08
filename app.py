import os
from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Environment setup
load_dotenv()

host = 'postgres'  # docker image name
port = 5432  # default postgres port
user = os.environ['POSTGRES_USER']
password = os.environ['POSTGRES_PASSWORD']
db = os.environ['POSTGRES_DB']

url = f'postgresql://{user}:{password}@{host}:{port}/{db}'

# Flask init
app = Flask(__name__)

# SQLAlchemy setup
app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # disable random logs
db = SQLAlchemy(app)

# Setup Flask Migrate
"""
IMPORTANT: commit migrations folder along with your code!!!
How to do migrations:
1. ssh into the docker image
    $ docker exec -it app sh

2. init flask migration (only first time)
    $ flask db init

3. perform migration (like git commit)
    $  flask db migrate -m "Initial migration."

4. apply changes
    $ flask db upgrade

Once applied, a new table "alembic_version" is created to track migrations 
"""
migrate = Migrate(app, db)

# Setup models


class AppleBuild(db.Model):
    build_id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.String(50))


def __init__(self, build_id, version):
    self.build_id = build_id
    self.version = version


# Only creates tables initially, use Flask migrate when updating table information
# Ref: https://flask-migrate.readthedocs.io/en/latest/
db.create_all()


@app.route('/v1/builds', methods = ['GET'])
def get_all_builds():
    # Query: https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_using_query.htm
    all = db.session.query(AppleBuild).all()
    return all

@app.route('/v1/builds/<build_id>', methods = ['GET'])
def get_build(build_id):
    build = db.session.query(AppleBuild).first(build_id=build_id)
    return build

@app.route('/v1/builds', methods = ['POST'])
def add_build():
    build_id = request.form.get('build_id')
    version = request.form.get('version')

    new_build = AppleBuild(build_id, version)
    db.session.add(new_build)
    db.session.commit()

    return new_build


if __name__ == '__main__':
    app.run()
