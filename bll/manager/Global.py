from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models.TimeSeriesPacket import Base as BasePacket
from models.Host import Base as BaseHost
from models.User import Base as BaseUser,User
from functools import wraps
from flask import request, jsonify
import jwt

# engine to connect to the database with TimescaleDB-specific options
engine = create_engine('postgresql://russo:mypassword5103@localhost:5432/postgres',
                       connect_args={'options': '-c timescaledb.telemetry_level=off'})

SECRET_KEY = "mykey"

# Check if timescaledb works
#engine.engine.e('CREATE EXTENSION IF NOT EXISTS timescaledb')

# tables in the database
BasePacket.metadata.create_all(engine)
# tables in the database
BaseHost.metadata.create_all(engine)
# tables in the database
BaseUser.metadata.create_all(engine)

def initialize_default_user():
    session = sessionMaker()
    try:
        # Check if the default user exists
        default_user = session.query(User).filter_by(username='admin').first()
        if not default_user:
            # Create the default user
            default_user = User(
                username='admin',
                role='admin',
                password="admin",
                created_at=datetime.now()
            )
            default_user.set_password('admin')  # Replace with a secure default password
            session.add(default_user)
            session.commit()
            print("Default admin user created.")
        else:
            print("Default admin user already exists.")
    except Exception as e:
        session.rollback()
        print(f"Error creating default user: {e}")
    finally:
        session.close()
        

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({"message": "Token is missing!"}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = data['user_id']
        except:
            return jsonify({"message": "Token is invalid!"}), 401
        return f(current_user, *args, **kwargs)
    return decorated

sessionMaker =  sessionmaker(autocommit=False, bind=engine)


    