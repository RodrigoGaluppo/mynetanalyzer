from sqlalchemy import Column, Integer, Text, DateTime, String
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TimeSeriesPacket(Base):
    __tablename__ = 'time_series_packet'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.now)  # timestamp of registry
    src = Column(String(50))
    dst = Column(String(50))
    timing = Column(String(30)) # timestamp of packet on delivery
    size = Column(String(10))
    protocol=Column(String(20))
    ip_address = Column(String(50))
    src_port = Column(String(10), default="")
    dst_port = Column(String(10), default="")

    def to_dict(self):
        return {
            "id": self.id,
            "src":self.src,
            "dst":self.dst,
            "protocol":self.protocol,
            "size":self.size,
            "timing":self.timing,
            "timestamp": self.timestamp,
            "ip_address": self.ip_address,
            "src_port":self.src_port,
            "dst_port":self.dst_port
        }
