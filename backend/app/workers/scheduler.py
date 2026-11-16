import logging
from datetime import datetime, timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select
from app.database.session import AsyncSessionLocal
from app.models.tracking import PriceAlert
from app.models.marketplaces import MarketplaceListing

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


async def evaluate_price_alerts_job():
    """Background task to evaluate all active price alerts against current marketplace prices."""
    logger.info("Running background price alert evaluation...")
    try:
        async with AsyncSessionLocal() as session:
            stmt = (
                select(PriceAlert, MarketplaceListing)
                .join(MarketplaceListing, MarketplaceListing.variant_id == PriceAlert.variant_id)
                .where(PriceAlert.is_active == True, PriceAlert.is_triggered == False)
            )
            res = await session.execute(stmt)
            alerts_evaluated = 0
            alerts_triggered = 0

            for alert, listing in res.all():
                alerts_evaluated += 1
                if float(listing.current_price) <= float(alert.target_price):
                    alert.is_triggered = True
                    alert.triggered_at = datetime.now(timezone.utc)
                    alerts_triggered += 1
                    logger.info(f"Price alert {alert.id} triggered: target={alert.target_price}, current={listing.current_price}")

            if alerts_triggered > 0:
                await session.commit()
            logger.info(f"Alert evaluation complete: {alerts_evaluated} evaluated, {alerts_triggered} triggered.")
    except Exception as e:
        logger.error(f"Error during price alert evaluation: {e}")


def start_scheduler():
    if not scheduler.running:
        scheduler.add_job(
            evaluate_price_alerts_job,
            "interval",
            minutes=15,
            id="price_alert_checker",
            replace_existing=True,
        )
        scheduler.start()
        logger.info("APScheduler background worker started.")


def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("APScheduler background worker stopped.")
