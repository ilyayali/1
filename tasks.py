import logging
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab

from src.database import Database
from src.parcer import get_feedbackPoints_and_total_price

# Настройки
broker_url = "redis://redis:6379/0"
result_backend = "redis://redis:6379/0"
timezone = "UTC"

app = Celery("tasks", broker=broker_url, backend=result_backend, timezone=timezone)

beat_schedule = {
    "updating_the_database_every_hour": {
        "task": "tasks.updating_the_database",
        "schedule": crontab(minute=0),  # Задача будет запускаться каждый час
    }
}


@app.task
def updating_the_database():
    """Фоновая задача наполнения базы данных"""
    with Database("src/data.db") as db:
        db.create_table()
        for product in get_feedbackPoints_and_total_price():
            db.insert_product(product=product)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Запуск задачи сразу после старта
    sender.add_periodic_task(
        timedelta(seconds=1), updating_the_database.s(), name="initial_task"
    )
