#!/usr/bin/python3
# coding: utf-8
# Copyright (c) 2019-2020 Latona. All rights reserved.

from aion.mysql import BaseMysqlAccess
from aion.logger import lprint_exception


class JobSchedulerDB(BaseMysqlAccess):
    def __init__(self):
        super().__init__("Maintenance")
    def get_microservice_name(self, job_id):
        query = f"""
            SELECT 
                jm.microservice_id, 
                jm.microservice_name
            FROM Maintenance.job job
            INNER JOIN Maintenance.job_microservice jm
                ON job.microservice_id = jm.microservice_id
            WHERE job.job_id = {job_id};
        """
        result = self.get_query(query)
        if result:
            return result.get('microservice_name')
        else:
            return ''

    def get_microservice_list(self):
        query = f"""
            SELECT 
                microservice_id, 
                microservice_name
            FROM Maintenance.job_microservice;
        """
        return self.get_query_list(100, query)

    def get_current_schedules(self, job_ids):
        job_ids_str = '('+','.join(list(set(job_ids)))+')'
        query = f"""
            SELECT 
                js.project_id as project_id,
                js.microservice_id as microservice_id,
                js.schedule_id as schedule_id,
                jm.microservice_name as microservice_name
            FROM Maintenance.jobschedule js 
            INNER JOIN Maintenance.job_microservice jm 
            ON js.microservice_id = jm.microservice_id
            where js.job_id IN {job_ids_str};
        """
        return self.get_query_list(100, query)


    def delete_current_equipments(self, job_ids):
        job_ids_str = '('+','.join(list(set(job_ids)))+')'
        query = f"""
            DELETE FROM Maintenance.equipments_has_jobs WHERE job_id IN {job_ids_str};
        """
        ret = self.set_query(query)
        if not ret:
            lprint_exception('failed to delete data')
        else:
            self.commit_query()
        
    def delete_current_schedules(self, job_ids):
        job_ids_str = '('+','.join(list(set(job_ids)))+')'
        query = f"""
            DELETE FROM Maintenance.jobschedule WHERE job_id IN {job_ids_str};
        """
        ret = self.set_query(query)
        if not ret:
            lprint_exception('failed to delete data')
        else:
            self.commit_query()

    def set_schedule(self, project_id, microservice_id, schedule_id, \
            job_id, job_name, start_at, stop_at, repeat_type, cron_date ):
        query = f"""
            INSERT INTO Maintenance.jobschedule (project_id, microservice_id, schedule_id,
                job_id, job_name, start_at, stop_at, repeat_type, cron_date) 
            VALUES ({int(project_id)}, {int(microservice_id)}, {int(schedule_id)},
                {int(job_id)}, '{job_name}', '{start_at}', '{stop_at}',
                {int(repeat_type)}, '{cron_date}');
        """

        ret = self.set_query(query)
        if not ret:
            lprint_exception('failed to insert data')
        else:
            self.commit_query()

    def set_equipments(self, job_id, equipment_list):
        query = f"""
                insert into Maintenance.equipments_has_jobs(job_id, equipment_id)
                values 
                """
        for equipment_id in equipment_list:
            tmp = "(%d, %d)," % (job_id, equipment_id)
            query += tmp
        query = query[:-1] + ";"

        ret = self.set_query(query)
        if not ret:
            lprint_exception('failed to insert data')
        else:
            self.commit_query()


