from django_cron import CronJobBase, Schedule
import requests

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'app.my_cron_job.do'    # a unique code

    def do(self):
        url = 'http://localhost:8000/usuarios/'
        cookie = 'django-insecure-82e32v=md3-ydr+ic4@f=pbi4yxe@zf@p$4by5npv+w@3(41'

            #use the 'cookies' parameter to send cookies to the server:
        x = requests.get(url, cookies = {"jwt": cookie})
        return cookie