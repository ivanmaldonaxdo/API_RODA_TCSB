from django_cron import CronJobBase, Schedule

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 5 # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'apps.tasks.my_cron_job'    # a unique code

    print("asi es, funciona")