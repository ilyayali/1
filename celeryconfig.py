from celery.schedules import crontab

broker_url = "redis://localhost:6379/0"
result_backend = "redis://localhost:6379/0"
timezone = "UTC"

beat_schedule = {
    "updating_the_database_every_hour": {
        "task": "tasks.updating_the_database",
        "schedule": crontab(
            minute="*"
        ),  # для запуска каждый час исправьте на minute=0, сейчас стоит тестовый параметр
    }
}
