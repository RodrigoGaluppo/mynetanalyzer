from sqlalchemy import Column, Integer, Text, DateTime, String
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class HostModel(Base):
    __tablename__ = 'host'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(50))
    name = Column(String(20))
    created_at=Column(DateTime, default=datetime.now)

    def to_dict(self):
        return {
            "id": self.id,
            "ip":self.ip,
            "name":self.name,
            "created_at":self.created_at
        }
