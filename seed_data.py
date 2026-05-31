import sys
import os
import datetime

# Add app to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.database import SessionLocal, engine
from backend.app import models

def seed_data():
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Check if empty
    if db.query(models.Event).count() > 0:
        print("Database already has data. Skipping seed.")
        return

    print("Seeding database with highly realistic global intelligence data...")
    
    # 1. Commodities
    commodities = [
        models.Commodity(name="Semiconductor", category="Technology"),
        models.Commodity(name="Lithium", category="Energy"),
        models.Commodity(name="Copper", category="Metals"),
        models.Commodity(name="Neon Gas", category="Materials")
    ]
    db.add_all(commodities)
    db.flush()

    # 2. Countries
    countries = [
        models.Country(name="Taiwan"),
        models.Country(name="Chile"),
        models.Country(name="DRC"),
        models.Country(name="Ukraine")
    ]
    db.add_all(countries)
    db.flush()

    now = datetime.datetime.utcnow()

    # 3. Articles & Events
    data = [
        {
            "title": "Major disruption at Hsinchu Science Park due to sudden power outage",
            "url": "https://example.com/taiwan-power",
            "source": "reuters.com",
            "com": commodities[0].id,
            "cty": countries[0].id,
            "org": "TSMC",
            "risk": "Factory Shutdown",
            "sev": "Critical",
            "sum": "A massive power outage hit the Hsinchu Science Park, completely halting production of advanced 3nm and 5nm nodes. Wafer spoilage expected to be significant.",
            "score": 95
        },
        {
            "title": "Chilean port workers announce indefinite strike affecting lithium exports",
            "url": "https://example.com/chile-strike",
            "source": "bloomberg.com",
            "com": commodities[1].id,
            "cty": countries[1].id,
            "org": "Port Workers Union",
            "risk": "Labor Strike",
            "sev": "High",
            "sum": "Logistics operations at major Chilean ports have ceased following failed negotiations. Lithium carbonate shipments to battery manufacturers delayed indefinitely.",
            "score": 75
        },
        {
            "title": "Severe flooding in the DRC copper belt blocks transport routes",
            "url": "https://example.com/drc-flood",
            "source": "aljazeera.com",
            "com": commodities[2].id,
            "cty": countries[2].id,
            "org": "Mining Corp",
            "risk": "Natural Disaster",
            "sev": "Moderate",
            "sum": "Unprecedented rainfall has washed out key logistical arteries in the copper belt. Supply bottlenecks are expected to ripple through the global market over the next week.",
            "score": 45
        },
        {
            "title": "Neon gas purification plant damaged in conflict zone",
            "url": "https://example.com/neon-supply",
            "source": "wsj.com",
            "com": commodities[3].id,
            "cty": countries[3].id,
            "org": "Cryoin",
            "risk": "War",
            "sev": "Critical",
            "sum": "A crucial neon gas purification facility responsible for 20% of the world's semiconductor-grade neon was severely damaged during recent escalations.",
            "score": 98
        }
    ]

    for item in data:
        art = models.Article(
            gdelt_id=item["url"],
            url=item["url"],
            title=item["title"],
            text=item["sum"],
            source=item["source"],
            published_date=now,
            processed=True
        )
        db.add(art)
        db.flush()

        evt = models.Event(
            article_id=art.id,
            commodity_id=item["com"],
            country_id=item["cty"],
            organization=item["org"],
            event_type=item["risk"],
            risk_type=item["risk"],
            severity_label=item["sev"],
            summary=item["sum"],
            event_date=now
        )
        db.add(evt)
        db.flush()

        score = models.RiskScore(
            event_id=evt.id,
            score=item["score"],
            level=item["sev"]
        )
        db.add(score)

        if item["sev"] in ["Critical", "High"]:
            alert = models.Alert(
                event_id=evt.id,
                title=f"{item['sev']} Risk: {item['risk']} detected",
                message=item["sum"]
            )
            db.add(alert)
    
    db.commit()
    print("Seeding complete.")

if __name__ == "__main__":
    seed_data()
