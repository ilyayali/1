from celery import Celery

from src.database import Database
from src.parcer import get_feedbackPoints_and_total_price

app = Celery("tasks")
app.config_from_object("celeryconfig")


@app.task
def updating_the_database():
    """Фоновая задача наполнения базы данных"""
    with Database("data.db") as db:
        db.create_table()
        for product in get_feedbackPoints_and_total_price():
            db.insert_product(product=product)
