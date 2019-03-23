from django.apps import AppConfig


class JapanConfig(AppConfig):
    name = 'japan'

    # def ready(self):
    #     from kanjiUpdate import updater
    #     updater.start()
