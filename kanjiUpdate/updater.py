from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from kanjiUpdate import updateKanjiApi

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(updateKanjiApi.update_kanji, 'interval', minutes=1)
    scheduler.start()