import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from .nlp.pipeline import process_and_store_articles
from .database import SessionLocal

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()

def scheduled_gdelt_job():
    logger.info("Running scheduled GDELT ingestion job...")
    db = SessionLocal()
    try:
        process_and_store_articles(db)
    except Exception as e:
        logger.error(f"Error in scheduled job: {e}")
    finally:
        db.close()

def start_scheduler():
    if not scheduler.running:
        # Run immediately on startup
        scheduler.add_job(
            scheduled_gdelt_job,
            trigger='date',
            id='initial_run'
        )
        # Then run every 30 minutes
        scheduler.add_job(
            scheduled_gdelt_job,
            trigger=IntervalTrigger(minutes=30),
            id='gdelt_ingestion_job',
            replace_existing=True
        )
        scheduler.start()
        logger.info("Scheduler started.")

def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler stopped.")
