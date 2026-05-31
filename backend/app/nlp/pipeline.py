import requests
import json
import logging
import datetime
from sqlalchemy.orm import Session
from .. import models
from bs4 import BeautifulSoup

# NLP Libraries
import spacy
from langdetect import detect
from deep_translator import GoogleTranslator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

logger = logging.getLogger(__name__)

# Attempt to load spacy model, fallback to download if not present
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    logger.warning("spacy en_core_web_sm not found. Please run 'python -m spacy download en_core_web_sm'. Proceeding without NER or using a placeholder.")
    nlp = None

analyzer = SentimentIntensityAnalyzer()

CORE_COMMODITIES = [
    "Semiconductor", "Semiconductors", "Rare Earth", "Lithium", 
    "Copper", "Fertilizer", "Fertilizers", "Pharmaceutical", "Crude Oil", "Natural Gas"
]

RISK_TYPES = [
    "Export Restriction", "Sanctions", "Port Congestion", "Shipping Disruption",
    "Factory Shutdown", "Mine Shutdown", "Natural Disaster", "Earthquake",
    "Flood", "Hurricane", "Political Conflict", "War", "Trade Restriction",
    "Energy Crisis", "Labor Strike", "Regulatory Action", "Shortage"
]

def fetch_gdelt_articles():
    """
    Fetch articles from GDELT DOC 2.0 API.
    """
    logger.info("Fetching articles from GDELT...")
    # GDELT DOC 2.0 API query for our topics
    query = '("semiconductor shortage" OR "chip manufacturing delay" OR "rare earth shortage" OR "lithium supply" OR "copper mine shutdown" OR "fertilizer shortage" OR "port congestion" OR "factory shutdown" OR "labor strike")'
    url = f"https://api.gdeltproject.org/api/v2/doc/doc?query={query}&mode=artlist&maxrecords=50&format=json"
    
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            return data.get("articles", [])
        else:
            logger.error(f"Failed to fetch GDELT: {response.status_code}")
            return []
    except Exception as e:
        logger.error(f"Error fetching GDELT: {e}")
        return []

def clean_text(html_text):
    if not html_text:
        return ""
    soup = BeautifulSoup(html_text, "html.parser")
    return soup.get_text(separator=" ").strip()

def detect_and_translate(text):
    if not text:
        return text
    try:
        lang = detect(text)
        if lang != 'en':
            translator = GoogleTranslator(source='auto', target='en')
            # Chunking might be required for long text, but we'll do simple translation for MVP
            text = translator.translate(text[:4000]) 
    except Exception as e:
        logger.warning(f"Translation/Language detection failed: {e}")
    return text

def extract_entities_and_risks(text):
    """
    Use spaCy and heuristics to extract structured data.
    """
    result = {
        "commodity": None,
        "country": None,
        "organization": None,
        "risk_type": None,
        "severity": "Low",
        "summary": text[:200] + "..." if len(text) > 200 else text
    }
    
    # 1. Commodity Detection (Heuristics)
    text_lower = text.lower()
    for c in CORE_COMMODITIES:
        if c.lower() in text_lower:
            result["commodity"] = c
            break
            
    # 2. Risk Type Detection (Heuristics)
    for r in RISK_TYPES:
        if r.lower() in text_lower:
            result["risk_type"] = r
            break
    
    # 3. Country and Organization Detection (spaCy NER)
    if nlp:
        doc = nlp(text)
        orgs = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
        gpes = [ent.text for ent in doc.ents if ent.label_ == "GPE"]
        
        if orgs:
            result["organization"] = orgs[0] # Take the first prominent ORG
        if gpes:
            result["country"] = gpes[0]      # Take the first prominent GPE
            
    # 4. Severity Scoring (VADER + Heuristics)
    sentiment = analyzer.polarity_scores(text)
    compound = sentiment['compound']
    
    # If highly negative sentiment, higher severity
    if compound <= -0.6:
        result["severity"] = "Critical"
    elif compound <= -0.3:
        result["severity"] = "High"
    elif compound < 0:
        result["severity"] = "Moderate"
    else:
        # Check risk keywords that imply severity
        if any(w in text_lower for w in ["shutdown", "crisis", "disaster", "war"]):
            result["severity"] = "High"
        else:
            result["severity"] = "Low"
            
    return result

def calculate_risk_score(severity_label):
    scores = {
        "Low": 15,
        "Moderate": 40,
        "High": 65,
        "Critical": 90
    }
    return scores.get(severity_label, 15)

def process_and_store_articles(db: Session):
    articles = fetch_gdelt_articles()
    
    for art in articles:
        url = art.get('url')
        if not url:
            continue
            
        # Check if exists
        existing = db.query(models.Article).filter(models.Article.url == url).first()
        if existing:
            continue
            
        title = art.get('title', '')
        # GDELT artlist doesn't always give full text, we might just have a snippet/title
        raw_text = art.get('title', '') + " " + art.get('seendate', '') 
        
        # Clean & Translate
        clean_t = clean_text(title)
        english_t = detect_and_translate(clean_t)
        
        # Store Article
        db_article = models.Article(
            gdelt_id=art.get('urlid', url),
            url=url,
            title=english_t,
            text=english_t,
            source=art.get('domain', ''),
            published_date=datetime.datetime.utcnow()
        )
        db.add(db_article)
        db.flush()
        
        # Extract Entities
        extraction = extract_entities_and_risks(english_t)
        
        # We only create an event if a commodity or risk was found
        if extraction["commodity"] or extraction["risk_type"]:
            
            # Get or create commodity
            commodity_id = None
            if extraction["commodity"]:
                c = db.query(models.Commodity).filter(models.Commodity.name == extraction["commodity"]).first()
                if not c:
                    c = models.Commodity(name=extraction["commodity"], category="General")
                    db.add(c)
                    db.flush()
                commodity_id = c.id
                
            # Get or create country
            country_id = None
            if extraction["country"]:
                cty = db.query(models.Country).filter(models.Country.name == extraction["country"]).first()
                if not cty:
                    cty = models.Country(name=extraction["country"])
                    db.add(cty)
                    db.flush()
                country_id = cty.id
                
            # Create Event
            db_event = models.Event(
                article_id=db_article.id,
                commodity_id=commodity_id,
                country_id=country_id,
                organization=extraction["organization"],
                event_type=extraction["risk_type"] or "General Disruption",
                risk_type=extraction["risk_type"] or "General Disruption",
                severity_label=extraction["severity"],
                summary=extraction["summary"],
                event_date=datetime.datetime.utcnow()
            )
            db.add(db_event)
            db.flush()
            
            # Create Risk Score
            score_val = calculate_risk_score(extraction["severity"])
            db_score = models.RiskScore(
                event_id=db_event.id,
                score=score_val,
                level=extraction["severity"]
            )
            db.add(db_score)
            
            # Create Alert if High or Critical
            if extraction["severity"] in ["High", "Critical"]:
                db_alert = models.Alert(
                    event_id=db_event.id,
                    title=f"{extraction['severity']} Risk: {db_event.event_type} in {extraction['country'] or 'Unknown Region'}",
                    message=f"Detected a {extraction['severity'].lower()} risk regarding {extraction['commodity'] or 'a critical resource'}."
                )
                db.add(db_alert)
        
        db_article.processed = True
        db.commit()
    
    logger.info("Finished processing GDELT articles.")
