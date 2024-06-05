import configparser
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 
from models.TimeSeriesPacket import Base as BasePacket
from models.Host import Base as BaseHost
from models.User import Base as BaseUser

config = configparser.ConfigParser()
config.read('default.conf')

database_url = config.get('DEFAULT', 'database_url')
timescaledb_telemetry_level = config.get('DEFAULT', 'timescaledb_telemetry_level')


engine = create_engine(database_url,
                       connect_args={'options': f'-c timescaledb.telemetry_level={timescaledb_telemetry_level}'})


BasePacket.metadata.create_all(engine)
BaseHost.metadata.create_all(engine)
BaseUser.metadata.create_all(engine)

sessionMaker =  sessionmaker(autocommit=False, bind=engine)

