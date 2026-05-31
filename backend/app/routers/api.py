from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from ..database import get_db
from .. import models

router = APIRouter()

@router.get("/articles")
def get_articles(db: Session = Depends(get_db), limit: int = 50):
    return db.query(models.Article).order_by(models.Article.published_date.desc()).limit(limit).all()

@router.get("/events")
def get_events(db: Session = Depends(get_db), limit: int = 50):
    return db.query(models.Event).order_by(models.Event.event_date.desc()).limit(limit).all()

@router.get("/alerts")
def get_alerts(db: Session = Depends(get_db), limit: int = 10, active_only: bool = True):
    query = db.query(models.Alert)
    if active_only:
        query = query.filter(models.Alert.is_active == True)
    return query.order_by(models.Alert.created_at.desc()).limit(limit).all()

@router.get("/risk-scores")
def get_risk_scores(db: Session = Depends(get_db), limit: int = 50):
    return db.query(models.RiskScore).order_by(models.RiskScore.calculated_at.desc()).limit(limit).all()

@router.get("/countries")
def get_countries(db: Session = Depends(get_db)):
    return db.query(models.Country).all()

@router.get("/commodities")
def get_commodities(db: Session = Depends(get_db)):
    return db.query(models.Commodity).all()

@router.get("/dashboard-summary")
def get_dashboard_summary(db: Session = Depends(get_db)):
    active_alerts = db.query(models.Alert).filter(models.Alert.is_active == True).count()
    critical_risks = db.query(models.RiskScore).filter(models.RiskScore.level == "Critical").count()
    
    # Affected countries count (countries with events in last 30 days)
    affected_countries = db.query(models.Country).join(models.Event).filter(
        models.Event.severity_label.in_(["High", "Critical"])
    ).distinct().count()
    
    # Top risks
    top_risks = db.query(models.Event).join(models.RiskScore).order_by(
        models.RiskScore.score.desc()
    ).limit(5).all()

    # Commodity rankings
    commodity_rankings = db.query(
        models.Commodity.name, 
        func.count(models.Event.id).label('incident_count')
    ).join(models.Event).group_by(models.Commodity.id).order_by(
        func.count(models.Event.id).desc()
    ).limit(5).all()

    return {
        "active_alerts": active_alerts,
        "critical_risks": critical_risks,
        "affected_countries": affected_countries,
        "top_risks": [
            {
                "id": r.id,
                "commodity": r.commodity.name if r.commodity else None,
                "country": r.country.name if r.country else None,
                "severity": r.severity_label,
                "type": r.event_type
            } for r in top_risks
        ],
        "commodity_rankings": [{"name": c[0], "incidents": c[1]} for c in commodity_rankings]
    }
