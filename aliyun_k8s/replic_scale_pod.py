#! /usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import sys
from os import path
from kubernetes import client, config
from pprint import pprint
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from aliyun_k8s.conf import setting




class Pod_scale(object):
    def __init__(self, args):
        self.time = args

    def replic_set_scale(self):

        kube_config = path.join(path.dirname(__file__),"kubeconfig.yaml")
        config.load_kube_config(config_file=kube_config)
        api_instance = client.AppsV1Api()

        for app_name,app_scale in self.time.items():

            body = {'spec': {'replicas': app_scale}}

            api_response = api_instance.patch_namespaced_deployment(app_name, 'default', body)
            pprint(api_response)


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--time", "-t", type=str, required=True, help="不同时间段的容器个数")
    args_options = parser.parse_args()
    return args_options


if __name__ == '__main__':
    args = arg_parse()
    if args.time == 'ten':
        k8s = Pod_scale(setting.ten_scale)
        k8s.replic_set_scale()
    elif args.time == 'usually':
        k8s = Pod_scale(setting.usually_scale)
        k8s.replic_set_scale()

