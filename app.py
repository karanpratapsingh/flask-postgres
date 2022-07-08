import os
from dataclasses import dataclass

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

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


@dataclass
class AppleBuild(db.Model):
    build_id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.String(50))


def __init__(self, build_id, version):
    self.build_id = build_id
    self.version = version


# Only creates tables initially, use Flask migrate when updating schema
# Ref: https://flask-migrate.readthedocs.io/en/latest/
db.create_all()


@app.route('/')
def hello_world():
    return 'Hello world!'


@app.route('/v1/builds', methods=['GET'])
def get_all_builds():
    # Query: https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_using_query.htm
    all = AppleBuild.query.all()
    return jsonify(builds=[{'build_id': build.build_id, 'version': build.version} for build in all])


@app.route('/v1/builds/<build_id>', methods=['GET'])
def get_build(build_id):
    build = AppleBuild.query.filter_by(build_id=build_id).first()

    if not build:
        return jsonify(error=f'Build with id: {build_id} not found')
    return jsonify(build_id=build.build_id, version=build.version)


@app.route('/v1/builds', methods=['POST'])
def add_build():
    # Get value from the POST request (Form data)
    version = request.form.get('version')

    if not version:
        return jsonify(error='version is required')

    # We don't need to explicitly give id as it's auto-incremented
    new_build = AppleBuild(version=version)

    # Add new changes to the database
    db.session.add(new_build)
    db.session.commit()

    return jsonify(build_id=new_build.build_id, version=new_build.version)


if __name__ == '__main__':
    app.run(host="0.0.0.0")
