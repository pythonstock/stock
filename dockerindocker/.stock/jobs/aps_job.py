#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
from pytz import utc
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.blocking import BlockingScheduler

from apscheduler.executors.pool import ProcessPoolExecutor
import libs.common as common

# doc : http://apscheduler.readthedocs.io/en/latest/modules/jobstores/sqlalchemy.html
jobstores = {
    'default': SQLAlchemyJobStore(url=common.MYSQL_CONN_URL, tablename='apscheduler_jobs')
}
executors = {
    'default': {'type': 'threadpool', 'max_workers': 20},
    'processpool': ProcessPoolExecutor(max_workers=5)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}
scheduler = BlockingScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)
scheduler.start()
print("start ...")
