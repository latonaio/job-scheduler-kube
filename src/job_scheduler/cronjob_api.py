#!/usr/bin/python3
# coding: utf-8
# Copyright (c) 2019-2020 Latona. All rights reserved.

from kubernetes import client, config
import yaml
import os

from aion.logger import lprint, lprint_exception
from .client_base import get_client_base

NAMESPACE = 'default'


class CronJob():
    def __init__(self):
        self.api_instance = client.BatchV1beta1Api(get_client_base())

    def getCurrentCronjobs(self, microservice_name):
        match_list = []
        try:
            api_response = self.api_instance.list_cron_job_for_all_namespaces()
            lprint(f"BatchV1beta1Api->list_cron_job_for_all_namespaces is successful.")
            lprint(api_response)
            for row in api_response.items:
                lprint(row)
                name = row.metadata.name
                if microservice_name in name:
                    match_list.append(name)
        except client.rest.ApiException as e:
            lprint_exception("Exception when calling BatchV1beta1Api->list_cron_job_for_all_namespaces: %s\n" % e)
        return match_list

    def createCronJob(self, job_id, name, image, schedule, ms_number, envoy_name ):
        body = None
        with open('yaml/cronjob.yaml', 'r') as f:
            body = yaml.full_load(f)
        aion_home = os.environ.get("AION_HOME")
        
        if body:
            # set cronjob name
            body['metadata']['name'] = name
            body['spec']['jobTemplate']['spec']['template']['spec']['containers'][0]['name'] = name
            # set docker image name 
            body['spec']['jobTemplate']['spec']['template']['spec']['containers'][0]['image'] = f'{image}:latest'

            # set execute schedule as cron time format
            body['spec']['schedule'] = schedule

            # set env
            env = body['spec']['jobTemplate']['spec']['template']['spec']['containers'][0]['env']
            for row in env:
                if row.get('name') == 'MS_NUMBER':
                    row['value'] = str(ms_number)
                if row.get('name') == 'AION_HOME':
                    row['value'] = aion_home
            env.append({
                'name':'JOB_ID',
                'value': str(job_id)
            })

            # set envoy configmap name
            volumes = body['spec']['jobTemplate']['spec']['template']['spec']['volumes']
            for row in volumes:
                if row.get('configMap'):
                    row['configMap']['name'] = envoy_name

            try:
                api_response = self.api_instance.create_namespaced_cron_job(
                    NAMESPACE, body)
                lprint(f"BatchV1beta1Api->create_namespaced_cron_job for {name} is successful.")
            except client.rest.ApiException as e:
                lprint_exception("Exception when calling BatchV1beta1Api->create_namespaced_cron_job: %s\n" % e)

    def deleteCronJob(self, name):
        try:
            api_response = self.api_instance.delete_namespaced_cron_job(name, NAMESPACE)
            lprint(f"BatchV2alpha1Api->delete_namespaced_cron_job for {name} is successful.")
        except client.rest.ApiException as e:
            lprint_exception("Exception when calling BatchV2alpha1Api->delete_namespaced_cron_job: %s\n" % e)

