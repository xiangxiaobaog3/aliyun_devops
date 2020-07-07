#! /usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from kubernetes import client, config

kube_config = path.join(path.dirname(__file__),"kubeconfig.yaml")
config.load_kube_config(config_file=kube_config)

api_instance = client.AppsV1Api()

ret = api_instance.list_namespaced_deployment('default')

replic_num = []

for i in ret.items:
    relic_dict = {}
    relic_dict[i.metadata.name] = i.status.available_replicas
    replic_num.append(relic_dict)
    # scale_num = i.status.available_replicas
    # replic_num = dict(zip(app_name, scale_num))

print(replic_num)