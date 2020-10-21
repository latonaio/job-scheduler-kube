#!/usr/bin/python3
# coding: utf-8
# Copyright (c) 2019-2020 Latona. All rights reserved.

import os
from kubernetes import client, config


def get_client_base():
    if os.path.exists(os.environ.get("HOME")+"/.kube/config"):
        config.load_kube_config()
        return client.CoreV1Api()

    configuration = client.Configuration()
    configuration.verify_ssl = True
    configuration.host = "https://" + \
        os.environ.get("KUBERNETES_SERVICE_HOST")
    configuration.api_key["authorization"] = _get_token()
    configuration.api_key_prefix["authorization"] = "Bearer"
    configuration.ssl_ca_cert = "/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"
    return client.ApiClient(configuration)

def _get_token():
    with open("/var/run/secrets/kubernetes.io/serviceaccount/token") as f:
        return f.read()
