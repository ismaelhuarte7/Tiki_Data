from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()

def init_scheduler(app):
    """
    Inicializa el scheduler para tareas programadas.
    Se ejecuta cada hour para cerrar votaciones MVP expiradas.
    """
    from src.services.match_service import MatchService

    def job_finalize_mvp_votes():
        with app.app_context():
            try:
                count = MatchService.finalize_expired_mvp_votes()
                if count > 0:
                    logger.info(f"Se finalizaron {count} votaciones MVP expiradas")
            except Exception as e:
                logger.error(f"Error en job finalize_mvp_votes: {e}")

    scheduler.add_job(
        func=job_finalize_mvp_votes,
        trigger=IntervalTrigger(hours=1),
        id='finalize_mvp_votes',
        name='Finalizar votaciones MVP expiradas',
        replace_existing=True,
        next_run_time=datetime.now() + timedelta(minutes=1)
    )

    scheduler.start()
    logger.info("Scheduler inicializado - job finalize_mvp_votes configurado")


def shutdown_scheduler():
    """Detiene el scheduler gracefully al cerrar la aplicación"""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler detenido")