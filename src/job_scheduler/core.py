#!/usr/bin/python3
# coding: utf-8
# Copyright (c) 2019-2020 Latona. All rights reserved.

from datetime import datetime
from time import sleep

from aion.microservice import main_decorator, Options
from aion.kanban import Kanban
from aion.logger import lprint, lprint_exception
from google.protobuf.json_format import MessageToDict

from .job_scheduler_db import JobSchedulerDB
from .cronjob_api import CronJob
from .configmap_api import ConfigMap

SERVICE_NAME = "job-scheduler"


def get_new_schedules(schedule_list, microservice_list):
    new_schedules = []
    job_ids = []

    for row in schedule_list:
        project_id = row['project_id']
        job_id = row['job_id']
        job_name = row['job_name']
        equipment_list = row['equipment_list']
        job_ids.append(str(job_id))

        microservice_name = ''
        for ms in microservice_list:
            if microservice_id == ms['microservice_id']:
                microservice_name = ms['microservice_name']
                break

        if not microservice_name:
            lprint(f'microservice {microservice_id}: not found')
            continue

        count = 1
        for col in row['schedules']:
            schedule_id = count
            start_at = col['start_at']
            stop_at = col['stop_at']
            repeat_type = col['repeat_type']

            cronjob_name = f'{microservice_name}-job{schedule_id:03}'
            envoy_name = f'envoy-config-{microservice_name}-job{schedule_id:03}'
            cron_date = get_cron_date(start_at, repeat_type)
            tmp = {
                'project_id': project_id,
                'microservice_id': microservice_id,
                'schedule_id': schedule_id,
                'job_id': job_id,
                'job_name': job_name,
                'start_at': start_at,
                'stop_at': stop_at,
                'repeat_type': repeat_type,
                'microservice_name': microservice_name,
                'cronjob_name': cronjob_name,
                'envoy_name': envoy_name,
                'cron_date': cron_date,
            }
            new_schedules.append(tmp)
            count+=1

    return new_schedules, job_ids

@main_decorator(SERVICE_NAME)
def main(opt: Options):
    # get cache kanban
    conn = opt.get_conn()
    num = opt.get_number()
    kanban = conn.get_one_kanban(SERVICE_NAME, num)

    # get output data path
    data_path = kanban.get_data_path()

    # get metadata
    metadata = kanban.get_metadata()
    schedule_list = metadata.get('schedule_list')


    ######### main function #############
    job_id = int(schedule_list['job_id'])
    new_schedules = schedule_list['schedule']
    microservice_name = ''

    # get db conn
    with JobSchedulerDB() as db:
        microservice_name = db.get_microservice_name(job_id)

    if microservice_name=='':
        lprint(f'microservice is not set for the job: {job_id}')
        return

    cj = CronJob()
    cm = ConfigMap()

    # get old schedule from k8s-api
    old_schedule_list = cj.getCurrentCronjobs(microservice_name)

    # stop job schedule from cronjob
    for old_schedule_name in old_schedule_list:
        cronjob_name = f'{old_schedule_name}'
        envoy_name = f'envoy-config-{old_schedule_name}'
        cj.deleteCronJob(cronjob_name)
        cm.deleteEnvoy(envoy_name)

    sleep(10)

    # set job schedule to cronjob
    for row in new_schedules:
        schedule_id = int(row['schedule_id'])
        cron_date = row['cron_date']
        cronjob_name = f'{microservice_name}-job{schedule_id:03}'
        envoy_name = f'envoy-config-{microservice_name}-job{schedule_id:03}'

        cm.createEnvoy(envoy_name)
        cj.createCronJob(
            job_id,
            cronjob_name,
            microservice_name,
            cron_date,
            schedule_id,
            envoy_name)

    # output after kanban
    conn.output_kanban(
        result=True,
        connection_key="default",
        output_data_path=data_path,
        process_number=num,
    )

