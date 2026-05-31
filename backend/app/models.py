from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class Article(Base):
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    gdelt_id = Column(String, unique=True, index=True) # Unique identifier from GDELT
    url = Column(String, unique=True)
    title = Column(String, nullable=True)
    text = Column(Text, nullable=True)
    source = Column(String, nullable=True)
    published_date = Column(DateTime, nullable=True)
    processed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    events = relationship("Event", back_populates="article")

class Commodity(Base):
    __tablename__ = "commodities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    category = Column(String, nullable=True)
    
    events = relationship("Event", back_populates="commodity")

class Country(Base):
    __tablename__ = "countries"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    iso_code = Column(String, nullable=True)
    
    events = relationship("Event", back_populates="country")

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("articles.id"))
    commodity_id = Column(Integer, ForeignKey("commodities.id"), nullable=True)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=True)
    
    organization = Column(String, nullable=True)
    event_type = Column(String, index=True)
    risk_type = Column(String, index=True)
    severity_label = Column(String) # Low, Moderate, High, Critical
    summary = Column(Text)
    event_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    article = relationship("Article", back_populates="events")
    commodity = relationship("Commodity", back_populates="events")
    country = relationship("Country", back_populates="events")
    risk_score = relationship("RiskScore", back_populates="event", uselist=False)
    alerts = relationship("Alert", back_populates="event")

class RiskScore(Base):
    __tablename__ = "risk_scores"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    score = Column(Float) # 0 to 100
    level = Column(String) # Low, Moderate, High, Critical
    calculated_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    event = relationship("Event", back_populates="risk_score")

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    title = Column(String)
    message = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    event = relationship("Event", back_populates="alerts")
