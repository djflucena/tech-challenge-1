from sqlalchemy import Column, Text, Integer, DateTime, JSON, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class RawVitiviniculturaCurrent(Base):
    __tablename__ = "raw_vitivinicultura"
    __table_args__ = {"schema": "vitivinicultura"}

    endpoint   = Column(Text,    primary_key=True)
    ano        = Column(Integer, primary_key=True)
    subopcao   = Column(Text,    primary_key=True, nullable=True)
    fetched_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    payload    = Column(JSON,    nullable=False)
