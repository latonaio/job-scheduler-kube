#!/usr/bin/python3
# coding: utf-8
# Copyright (c) 2019-2020 Latona. All rights reserved.

from kubernetes import client, config
import yaml

from aion.logger import lprint, lprint_exception
from .client_base import get_client_base

NAMESPACE = 'default'


class ConfigMap():
    def __init__(self):
        self.api_instance = client.CoreV1Api(get_client_base())


    def createEnvoy(self, name):
        data = None
        with open('yaml/envoy.yaml', 'r') as f:
            data = f.read()

        body = {
            'data': {
                'envoy.yaml': data
            },
            'metadata': {
                'name': name
            }
        }

        if data:
            try:
                api_response = self.api_instance.create_namespaced_config_map(
                    NAMESPACE, body)
                lprint(f"CoreV1Api->create_namespaced_config_map for {name} is successful.")
            except client.rest.ApiException as e:
                lprint_exception("Exception when calling CoreV1Api->create_namespaced_config_map: %s\n" % e)

    def deleteEnvoy(self, name):
        try:
            api_response = self.api_instance.delete_namespaced_config_map(
                name, NAMESPACE)
            lprint(f"CoreV1Api->delete_namespaced_config_map for {name} is successful.")
        except client.rest.ApiException as e:
            lprint_exception("Exception when calling CoreV1Api->delete_namespaced_config_map: %s\n" % e)

